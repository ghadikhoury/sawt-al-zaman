"""The local song catalogue (catalog/songs.jsonl) and fuzzy search over it.

Each song: {"title", "artist", "url", "lines"}. search() takes the noisy lines heard from a clip and returns the songs
whose lyric lines they resemble (character-trigram TF-IDF). It is only a fast first try: if nothing convincing comes
back, the editing agent (an LLM) identifies the song itself.
"""
import json
import math
import pickle
from pathlib import Path

import numpy as np
from scipy import sparse

from arabic_text import phonetic

HERE = Path(__file__).parent
SONGS = HERE / "catalog" / "songs.jsonl"
INDEX = HERE / "catalog" / "index.pkl"
DIM = 1 << 18


def _h(g):
    v = 2166136261
    for ch in g:
        v = ((v ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return v % DIM


def _vec(keys):
    rows, cols, vals = [], [], []
    for r, k in enumerate(keys):
        t = " " + k + " "
        cnt = {}
        for i in range(len(t) - 2):
            j = _h(t[i:i + 3])
            cnt[j] = cnt.get(j, 0) + 1
        for j, c in cnt.items():
            rows.append(r); cols.append(j); vals.append(1.0 + math.log(c))
    return sparse.csr_matrix((vals, (rows, cols)), shape=(len(keys), DIM), dtype=np.float32)


def _unit(M):
    n = np.sqrt(np.asarray(M.multiply(M).sum(axis=1)).ravel()) + 1e-9
    return sparse.diags(1.0 / n).dot(M).tocsr()


class Catalog:
    def __init__(self):
        if not SONGS.exists():
            raise SystemExit("No song catalogue yet: create catalog/songs.jsonl (see the README), or skip `find` and pass the "
                             "lyrics yourself with  lyrics.py song <video> --lyrics FILE --title ... --artist ...")
        self.songs = [json.loads(l) for l in SONGS.read_text(encoding="utf-8").splitlines() if l.strip()]
        stamp = (SONGS.stat().st_mtime, len(self.songs))
        if INDEX.exists():
            try:
                d = pickle.loads(INDEX.read_bytes())
                if d["stamp"] == stamp:
                    self.owner, self.idf, self.MT = d["owner"], d["idf"], d["MT"]
                    return
            except Exception:
                pass
        keys, owner = [], []
        for si, s in enumerate(self.songs):
            ks = [phonetic(l) for l in s["lines"]]
            rows = {k for k in ks if len(k) >= 4} | {ks[i] + " " + ks[i + 1] for i in range(len(ks) - 1) if len(ks[i] + ks[i + 1]) <= 90}
            keys.extend(rows); owner.extend([si] * len(rows))
        M = _vec(keys)
        df = np.asarray((M > 0).sum(axis=0)).ravel()
        self.idf = (np.log((M.shape[0] + 1.0) / (df + 1.0)) + 1.0).astype(np.float32)
        self.owner = np.array(owner, dtype=np.int32)
        self.MT = _unit(M.multiply(self.idf).tocsr()).T.tocsr()
        INDEX.write_bytes(pickle.dumps({"stamp": stamp, "owner": self.owner, "idf": self.idf, "MT": self.MT}))

    def search(self, heard_lines, top_k=5, hit=0.62):
        hk = list(dict.fromkeys(k for k in (phonetic(l) for l in heard_lines) if len(k.split()) >= 2 and len(k) >= 6))
        if not hk:
            return []
        S = _unit(_vec(hk).multiply(self.idf).tocsr()).dot(self.MT).tocsr()
        n = len(self.songs)
        sims = np.zeros((len(hk), n), dtype=np.float32)
        for i in range(len(hk)):
            a, b = S.indptr[i], S.indptr[i + 1]
            np.maximum.at(sims[i], self.owner[S.indices[a:b]], S.data[a:b])
        # a phrase found in many songs ("يا ليل", "يا حبيبي") says little: weight heard lines by rarity
        w = np.clip(np.log((n + 1.0) / ((sims >= 0.8).sum(axis=1) + 1.0)) / math.log(n + 1.0), 0.15, 1.0)
        w = w * np.clip(np.array([len(k.split()) for k in hk]) / 4.0, 0.5, 1.0)
        score = (np.where(sims >= hit, sims, 0.0) * w[:, None]).sum(axis=0)
        out = []
        for si in np.argsort(-score)[: top_k * 8]:
            if score[si] <= 0 or len(out) >= top_k:
                break
            s = self.songs[si]
            # skip other copies of a song already listed (same lyrics from another site)
            ks = {phonetic(l) for l in s["lines"]}
            if any(len(ks & o["_ks"]) >= 0.3 * min(len(ks), len(o["_ks"])) for o in out):
                continue
            out.append({"index": int(si), "title": s["title"], "artist": s["artist"], "url": s["url"], "score": round(float(score[si]), 2),
                        "heard_lines_matched": int((sims[:, si] >= hit).sum()), "heard_lines": len(hk), "_ks": ks})
        for o in out:
            del o["_ks"]
        return out

    def add(self, title, artist, lines, url=""):
        """Add a song (found by the agent or given by the owner) so it is never searched for twice."""
        s = {"title": title, "artist": artist, "url": url or f"added://{title}|{artist}", "lines": lines}
        if any(o["url"] == s["url"] for o in self.songs):
            return
        with open(SONGS, "a", encoding="utf-8") as f:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
        self.songs.append(s)
