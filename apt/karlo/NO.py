# numbers overlap

__author__ = 'karlo'

from math import log


def calc_no(words1, words2):
    extract_numbers = lambda words: [w for w in words if w.isdigit() or w[0] == '-' and w[1:].isdigit()]
    n1 = set(extract_numbers(words1))  # set of numbers in the first sentence
    n2 = set(extract_numbers(words2))  # set of numbers in the second sentence
    return log(1 + len(n1) + len(n2)), 2 * len(n1 & n2) / (len(n1) + len(n2)), my_subset(n1, n2) or my_subset(n2, n1)


def my_subset(numbers1, numbers2):
    for n1 in numbers1:
        check_in = False
        for n2 in numbers2:
            # "the numbers that differ only in the number of decimal places are treated as equal"
            sn1 = to_str(n1)
            sn2 = to_str(n2)
            if n1 == n2 or (not (sn1 is None) and not (sn2 is None) and (sn1.startswith(sn2) or sn2.startswith(sn1))):
                check_in = True
                break
        if not check_in:
            return False
    return True


def to_str(n):
    s = str(n)
    i = s.find('.')
    if i != -1:
        return s[i:]
    else:
        return None