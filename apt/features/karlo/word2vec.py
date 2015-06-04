__author__ = 'karlo'

from gensim.models import Word2Vec


def calc_w2v_similarity(words):
    words1 = words[0]
    words2 = words[1]
    if len(words1) == 0 or len(words2) == 0:
        return 0
    sim = 0.0
    n = 0
    for w1 in words1:
        for w2 in words2:
            try:
                sim += w2v_model.similarity(w1, w2)
                n += 1
            except KeyError:
                pass
    sim /= n
    return [sim]

# w2v_model = Word2Vec.load_word2vec_format("features/karlo/GoogleNews-vectors-negative300.bin", binary=True)
w2v_model = Word2Vec.load_word2vec_format("features/karlo/vectors.6B.50d.txt", binary=False)