__author__ = 'kbiscanic'

import math


def _len_compress(l):
    return math.log(1. + l)


def _is_stock(x):
    return len(x) > 1 and x[0] == u'.' and x[1:].decode('utf8').isupper()


def _capitalized(s):
    return set(x[0] for x in s if len(x[0]) > 1 and x[0][0].decode('utf8').isupper() and x[0][-1] != u'.')


def _stocks(s):
    return set(x[0] for x in s if _is_stock(x[0]))


def named_overlap(sa, sb):
    named_a = _capitalized(sa)
    named_b = _capitalized(sb)

    if len(named_a) > 0 and len(named_b) > 0:
        both = len(named_a.intersection(named_b))
        if both > 0:
            p = float(both) / len(named_a)
            r = float(both) / len(named_b)
            return 2 * p * r / (p + r), 1.
        else:
            return _len_compress(len(named_a) + len(named_b)), 0.
    else:
        return _len_compress(len(named_a) + len(named_b)), 0.


def named_overlap_words(words):
    return named_overlap(words[0], words[1])


def stocks_overlap(sa, sb):
    stocks_a = _stocks(sa)
    stocks_b = _stocks(sb)

    if len(stocks_a) > 0 and len(stocks_b) > 0:
        both = len(stocks_a.intersection(stocks_b))
        if both > 0:
            p = float(both) / len(stocks_a)
            r = float(both) / len(stocks_b)
            return 2 * p * r / (p + r), 1.
        else:
            return _len_compress(len(stocks_a) + len(stocks_b)), 0.
    else:
        return _len_compress(len(stocks_a) + len(stocks_b)), 0.


def stocks_overlap_words(words):
    return stocks_overlap(words[0], words[1])
