Translation Evaluation
---------------------

Manaal Faruqui, mfaruqui@cs.cmu.edu

Pre-processing:-
- Lower-casing the data, tokenization

My translation evaluation takes the following features:-

(1) 1-gram, 2-gram, 3-gram, 4-gram precision

(2) 1-gram, 2-gram, 3-gram, 4-gram precision of Brown word clusters

(3) 1-gram recall

Classifier: LDA: Linear Discriminant Analysis

Running the code:-

python main.py data/lc_tok_train_h1-h2-ref data/train.gold clusters/clus_400 data/lc_tok_test_h1-h2-ref | ./grade
