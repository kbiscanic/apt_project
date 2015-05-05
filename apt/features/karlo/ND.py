# normalized differences

__author__ = 'karlo'

from features.karlo.WWO import calc_ic


# sentence length
def calc_nda(all_tokens):
    words1 = [x[0] for x in all_tokens[0]]
    words2 = [x[0] for x in all_tokens[1]]
    l1 = len(words1)
    l2 = len(words2)
    if l1 == 0 and l2 == 0:
        return [0]
    else:
        return [abs(l1 - l2) / float(max(l1, l2))]


# the aggregate word information content
def calc_ndc(all_tokens):
    words1 = [x[0] for x in all_tokens[0]]
    words2 = [x[0] for x in all_tokens[1]]
    ic1 = sum([calc_ic(w) for w in words1])
    ic2 = sum([calc_ic(w) for w in words2])
    if ic1 == 0 and ic2 == 0:
        return [0]
    else:
        return [abs(ic1 - ic2) / float(max(ic1, ic2))]