import sys
from collections import Counter

fWordDict = Counter()
eWordDict = Counter()

sentPairs = {}
eGivenFWordTransProb = Counter()

for line in sys.stdin:
    line = line.strip()
    f, e = line.split('|||')
    f = f.strip()
    f = 'NULL '+ f
    e = e.strip()
    
    sentPairs[(f,e)] = 0.0
    
    for fWord in f.split():
        fWordDict[fWord] += 1.0
    
    for eWord in e.split():
        eWordDict[eWord] += 1.0

    for eWord in e.split():
        for fWord in f.split():
            eGivenFWordTransProb[(eWord,fWord)] = 1.0
        
for i in range(0,6):
    
    eGivenFCount = Counter()
    fTotal = Counter()
    total_s = {}
    
    for j, (f, e) in enumerate(sentPairs):

	f = 'NULL '+f
        
        if j % 1000 == 0:
            sys.stderr.write(str(j)+' ')
        
        total_s = Counter()
            
        for eWord in e.split():
            for fWord in f.split():
                total_s[eWord] += eGivenFWordTransProb[(eWord,fWord)]
                
        for eWord in e.split():
            for fWord in f.split():
                eGivenFCount[(eWord,fWord)] += 1.0*eGivenFWordTransProb[(eWord,fWord)]/total_s[eWord] 
                fTotal[fWord] += 1.0*eGivenFWordTransProb[(eWord,fWord)]/total_s[eWord] 
                
    #for eWord in eWordDict:
    #    for fWord in fWordDict:
    for (eWord, fWord), prob in eGivenFWordTransProb.iteritems():
            eGivenFWordTransProb[(eWord,fWord)] = 1.0*eGivenFCount[(eWord,fWord)]/fTotal[fWord]
    
    sys.stderr.write('Iteration '+str(i+1)+' finished\n')
            
for (eWord, fWord), prob in eGivenFWordTransProb.iteritems():
    #if prob != 0 and prob != 1.0:
    print eWord, fWord, prob
