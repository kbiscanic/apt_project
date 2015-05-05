# numbers overlap

__author__ = 'karlo'

from math import log


def calc_no(all_tokens):
    words1 = [x[0] for x in all_tokens[0]]
    words2 = [x[0] for x in all_tokens[1]]
    extract_numbers = lambda words: [w for w in words if w.isdigit() or w[0] == '-' and w[1:].isdigit()]
    n1 = set(extract_numbers(words1))  # set of numbers in the first sentence
    n2 = set(extract_numbers(words2))  # set of numbers in the second sentence

    f1 = log(1 + len(n1) + len(n2))
    f2 = 0 if len(n1) + len(n2) == 0 else 2 * len(my_intersection(n1, n2)) / (len(n1) + len(n2))
    f3 = my_subset(n1, n2) or my_subset(n2, n1)
    return [f1, f2, f3]


def my_intersection(numbers1, numbers2):
    inter = set()
    for n1 in numbers1:
        check_in = False
        for n2 in numbers2:
            if equal(n1, n2):
                check_in = True
                break
        if check_in:
            inter.add(n1)
    return inter


def my_subset(numbers1, numbers2):
    for n1 in numbers1:
        check_in = False
        for n2 in numbers2:
            if equal(n1, n2):
                check_in = True
                break
        if not check_in:
            return False
    return True


# "the numbers that differ only in the number of decimal places are treated as equal"
def equal(n1, n2):
    sn1 = to_str(n1)
    sn2 = to_str(n2)
    return n1 == n2 or (not (sn1 is None) and not (sn2 is None) and (sn1.startswith(sn2) or sn2.startswith(sn1)))


def to_str(n):
    s = str(n)
    i = s.find('.')
    if i != -1:
        return s[i:]
    else:
        return None