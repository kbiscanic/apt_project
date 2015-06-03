# apt_project
Project

1) Potrebno je skinuti WordNet sa:
    http://www.nltk.org/nltk_data/packages/corpora/wordnet.zip
i staviti ga u folder:
    /data/nltk/corpora/wordnet/

2) skinuti
        http://www-nlp.stanford.edu/data/glove.6B.50d.txt.gz
   otpakirati u folder
        apt/features/karlo
   na pocetak fajla dodati liniju:
        400000 50
    (broj rijeci, dimenzija)

3) jagar,
    kod mene je dosta sporo sa drugim corpusima ali ako ti se da isprobavat onda isprobaj neke vece corpuse na
        https://github.com/3Top/word2vec-api#where-to-get-a-pretrained-models
    pod 'Where to get a pretrained model',
    s tim da ako zavrsava na .bin treba stavit 'binary=True' u zadnjoj liniji word2vec.py
    - u txt fajlove treba vjerojatno uvijek na pocetak dodat ovu liniju iz 2)