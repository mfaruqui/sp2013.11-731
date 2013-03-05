# harmonic_mean = (p*r)/(alpha*r+beta*p)
# higher alhpha --> more importance to precision
# higher beta --> more importance to recall

import sys
from porter import stem
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.lda import LDA
from math import exp

ALPHA = 1# int(sys.argv[3])
BETA = 4#int(sys.argv[4])

def get_precision_recall_harmonic_mean(wordsFound, wordsGold):

    commonWords = wordsFound & wordsGold
    precision = 1.0*len(commonWords)/len(wordsFound)
    recall = 1.0*len(commonWords)/len(wordsGold)

    if precision == 0 and recall == 0:
        return 0

    f_score = (precision*recall)/(ALPHA*recall + BETA*precision)

    return f_score

def read_word_clusters(wordClusterFile):

    wordClusters = {}
    for line in open(wordClusterFile, 'r'):
        line = line.strip()
	cluster, word, freq = line.split('\t')
	wordClusters[word] = cluster

    return wordClusters

def replace_word_by_clus(sentence, wordClusters):

    clusters = []
    for word in sentence.split():
        clusters.append(wordClusters[word])

    return ' '.join(clusters)

def replace_word_by_stems(wordList):
  
    stemList = []
    for word in wordList:
        stemList.append(stem(word))

    return set(stemList)

def get_precision(setFound, setGold):

   common = setFound & setGold
   if len(setFound) == 0:
      return 0.0
   else:
      return 1.0*len(common)/len(setFound)

def get_ngrams(sentence, n):

   ngrams = []
   words = sentence.split()
   for i in range(0,len(words)-n+1):
       ngrams.append(' '.join(words[i:i+n]))

   return ngrams

def get_brev_penalty(found, gold):

    if len(found.split()) > len(gold.split()):
	    return 1.0
    else:
	    return exp(1-1.*len(found.split())/len(gold.split()))

trainFile, ansFile, clusterFile, testFile = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
wordClusters = read_word_clusters(clusterFile)

X = []
Y = []
for line, ans in zip(open(trainFile,'r'), open(ansFile,'r')):

    line = line.strip()
    h1, h2, ref = line.split(' | | | ')

    h1 = h1.strip()
    h2 = h2.strip()
    ref = ref.strip()

    brevH1 = get_brev_penalty(h1, ref)
    brevH2 = get_brev_penalty(h2, ref)

    h1PrecList = [brevH1*get_precision(set(get_ngrams(h1,n)), set(get_ngrams(ref,n))) for n in range(1,5)]
    h2PrecList = [brevH2*get_precision(set(get_ngrams(h2,n)), set(get_ngrams(ref,n))) for n in range(1,5)]

    h1Clus = replace_word_by_clus(h1, wordClusters)
    h2Clus = replace_word_by_clus(h2, wordClusters)
    refClus = replace_word_by_clus(ref, wordClusters)

    brevH1Clus = get_brev_penalty(h1Clus, refClus)
    brevH2Clus = get_brev_penalty(h2Clus, refClus)

    h1ClusPrecList = [get_precision(set(get_ngrams(h1Clus,n)), set(get_ngrams(refClus,n))) for n in range(1,5)]
    h2ClusPrecList = [get_precision(set(get_ngrams(h2Clus,n)), set(get_ngrams(refClus,n))) for n in range(1,5)]
    
    fScoreH1 = get_precision_recall_harmonic_mean(set(h1.split()), set(ref.split()))
    fScoreH2 = get_precision_recall_harmonic_mean(set(h2.split()), set(ref.split()))

    if len(h1.split()) > len(ref.split()):
	    brevH1 = 0
    else:
	    brevH1 = exp(-1.*len(h1.split())/len(ref.split()))
   
    if len(h2.split()) > len(ref.split()):
	    brevH2 = 0
    else:
	    brevH2 = exp(-1.*len(h2.split())/len(ref.split()))

    X.append(h1PrecList + h1ClusPrecList + [fScoreH1] + h2PrecList + h2ClusPrecList + [fScoreH2])
    Y.append(int(ans))

#classifier = svm.SVC()
#classifier = GaussianNB()
#classifier = tree.DecisionTreeClassifier()
#classifier = MultinomialNB()
classifier = LDA()
#classifier = tree.DecisionTreeRegressor()
classifier.fit(X,Y)

X = []
Y = []
for line in open(testFile,'r'):

     line = line.strip()
     h1, h2, ref = line.split(' | | | ')

     h1 = h1.strip()
     h2 = h2.strip()
     ref = ref.strip()

     h1PrecList = [get_precision(set(get_ngrams(h1,n)), set(get_ngrams(ref,n))) for n in range(1,5)]
     h2PrecList = [get_precision(set(get_ngrams(h2,n)), set(get_ngrams(ref,n))) for n in range(1,5)]

     h1Clus = replace_word_by_clus(h1, wordClusters)
     h2Clus = replace_word_by_clus(h2, wordClusters)
     refClus = replace_word_by_clus(ref, wordClusters)

     h1ClusPrecList = [get_precision(set(get_ngrams(h1Clus,n)), set(get_ngrams(refClus,n))) for n in range(1,5)]
     h2ClusPrecList = [get_precision(set(get_ngrams(h2Clus,n)), set(get_ngrams(refClus,n))) for n in range(1,5)]
	
     fScoreH1 = get_precision_recall_harmonic_mean(set(h1.split()), set(ref.split()))
     fScoreH2 = get_precision_recall_harmonic_mean(set(h2.split()), set(ref.split()))

     if len(h1.split()) > len(ref.split()):
	brevH1 = 0
     else:
	brevH1 = exp(-1.*len(h1.split())/len(ref.split()))
						   
     if len(h2.split()) > len(ref.split()):
	brevH2 = 0
     else:
	brevH2 = exp(-1.*len(h2.split())/len(ref.split()))

     X.append(h1PrecList + h1ClusPrecList + [fScoreH1] + h2PrecList + h2ClusPrecList + [fScoreH2])

Y = classifier.predict(X)
for val in Y:
    print val
