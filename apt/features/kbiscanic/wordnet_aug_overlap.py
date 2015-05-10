# WordNet-Augmented Word Overlap

from nltk.corpus import wordnet

__author__ = 'kbiscanic'

_simmemo = {}


def _sim(a, b):
    if a == b:
        return 1.
    (x, y) = (max(a, b), min(a, b))
    if (x, y) in _simmemo:
        return _simmemo[(x, y)]
    s1 = wordnet.synsets(x)
    s2 = wordnet.synsets(y)
    sim = max([0.] + [w1.path_similarity(w2) for w1 in s1 for w2 in s2])
    _simmemo[(x, y)] = sim
    return sim


def _score(a, sb):
    score = 0.
    for b in sb:
        score = max(score, _sim(a, b))
        if score == 1.:
            return 1.
    return score


def _p(sa, sb):
    p = 0.
    if len(sa) == 0:
        return 0.
    for a in sa:
        p += _score(a, sb)
    return p / len(sa)


def wordnet_aug_overlap(sa, sb):
    p1 = _p(sa, sb)
    p2 = _p(sb, sa)
    if p1 + p2 > 0:
        return 2. * p1 * p2 / (p1 + p2)
    else:
        return 0.


def wordnet_aug_overlap_words(words):
    return wordnet_aug_overlap(words[0], words[1])