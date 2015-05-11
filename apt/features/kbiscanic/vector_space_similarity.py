__author__ = 'kbiscanic'

from collections import Counter
from scipy.linalg import norm

from features.karlo.WWO import calc_ic


def _lsa(s):
    w = Counter(s)
    return {x: w[x] for x in w}


def _lsaic(s):
    w = Counter(s)
    return {x: calc_ic(x) * w[x] for x in w}


def _cosine_sim(da, db):
    sol = 0.
    for key in set(da.keys()).intersection(db.keys()):
        sol += da[key] * db[key]
    if sol == 0:
        return 0.
    return abs(sol / norm(da.values()) / norm(db.values()))


def vector_space_similarity(sa, sb, ic=False):
    if ic:
        lsaa = _lsaic(sa)
        lsab = _lsaic(sb)
    else:
        lsaa = _lsa(sa)
        lsab = _lsa(sb)
    return _cosine_sim(lsaa, lsab)


def vector_space_similarity_words(words, ic=False):
    return vector_space_similarity(words[0], words[1], ic)