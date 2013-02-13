Code for German-English word alignment
--------------------------------------

Manaal Faruqui, mfaruqui@cs.cmu.edu

Pre-processing:-
- Lower-casing the data

My alignment model works in the following way:-

(1) Obtains the Translation table p(f|e) using IBM Model 1

(2) While picking up alignments instead of having a uniform probability
    I put an exponential penalty on picking up words which are far from
    the current position of the target word.
	
	Penalty = exp(-abs(i/n -j/m))
	
	Hence, p(a_i = j) = exp(-abs(i/n -j/m)) * p(t[i]|s[j])
    
     This gives me a full 10 point improvement over the baseline

(3) Lexical filtering:
    
    - Only punctuation can be aligned to a punctuation
    
    - Numerals can only be aligned to a numeral

(4) if the ratio of word length is lenRatio = deWord/enWord
      
	- then 0.2 <= lenRatio <= 4

Running the code:-

pypy make_trans_table.py < lower_cased_train_file > translationTable

pypy get_alignments.py translationTable lower_cased_train_file > output.txt
