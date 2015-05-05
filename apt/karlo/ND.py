# normalized differences

__author__ = 'karlo'

from WWO import calc_ic


# sentence length
def calc_nda(words1, words2):
    l1 = len(words1)
    l2 = len(words2)
    if l1 == 0 and l2 == 0:
        return 0
    else:
        return abs(l1 - l2) / max(l1, l2)


# the aggregate word information content
def calc_ndc(words1, words2):
    ic1 = calc_ic(words1)
    ic2 = calc_ic(words2)
    if ic1 == 0 and ic2 == 0:
        return 0
    else:
        return abs(ic1 - ic2) / max(ic1, ic2)