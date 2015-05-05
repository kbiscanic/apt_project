from collections import Counter

# vraca n-grame velicine n nad listom rijeci jedne recenice
def make_ngrams(words, n):
    ngrams = []
    if n > len(words):
        return ngrams
    for i in xrange(0, len(words) - n + 1):
        ngram = []
        for j in xrange(0, n):
            ngram.append(words[i + j])
        ngrams.append(tuple(ngram))
    return ngrams


# vraca ngram overlap znacajke za 2 liste rijeci (iz 1 primjera) i velicinu n n-grama
def calc_ngram_overlap(words, n):
    ngrams = [make_ngrams(words[0], n), make_ngrams(words[1], n)]
    if len(ngrams[0]) + len(ngrams[1]) > 0:
        overlap_count = 0
        counter = Counter(ngrams[0])
        for ngram in ngrams[1]:
            if counter[ngram] > 0:
                overlap_count += 1
                counter[ngram] -= 1
        return 2 * overlap_count / float(len(ngrams[0]) + len(ngrams[1]))
    else:
        return 0
