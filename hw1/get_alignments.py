import sys
from math import exp
from leven import levenshtein
import string

tableFile = sys.argv[1]
inputFile = sys.argv[2]

transTable = {}
for line in open(tableFile,'r'):
	line = line.strip()

	en, fr, prob = line.split()
	prob = float(prob)
	en = en.strip()
	fr = fr.strip()
	transTable[(en,fr)] = prob

lineNum = 0
for line in open(inputFile,'r'):
	lineNum += 1

	line = line.strip()
	fr, en = line.split('|||')
	en = en.strip()
	fr = fr.strip()

	enLen = len(en.split())
	frLen = len(fr.split())

	if lineNum %5000 == 0:
		sys.stderr.write(str(lineNum)+' ')

	for i, eWord in enumerate(en.split()):
		prev = 0
		levenList = []
		frWords = fr.split()
		for j, fWord in enumerate(frWords):
			#levenList.append(2.0*levenshtein(eWord,fWord)/(enLen+frLen))
			val = transTable[(eWord,fWord)]
			val *= exp(-1*abs(1.0*i/enLen - 1.0*j/frLen))
			if val > prev:
				best = j
				prev = val

		#minLevenRatio = min(levenList)
		#if minLevenRatio < 0.05 and prev < 0.05:
		#bestLeven = levenList.index(minLevenRatio)

		if transTable[(eWord,'NULL')] > prev:
			#if minLevenRatio < 0.01:
			#	print str(bestLeven)+'-'+str(i),
			#else:
			pass
		elif (eWord in string.punctuation and frWords[best] in string.punctuation) or \
			(eWord not in string.punctuation and frWords[best] not in string.punctuation):
			frWord = frWords[best]
			for ch in ',.-':
				frWord = frWord.replace(ch,'')
				eWord = eWord.replace(ch,'')
			if (frWord.isdigit() and eWord.isdigit()) or not (frWord.isdigit() or eWord.isdigit()):
				if len(eWord) >= 1 and len(frWord) >= 1:
					lenRatio = 1.0*len(eWord)/len(frWord)
					if lenRatio <= 4 and lenRatio >= 0.1:
						print str(best)+'-'+str(i),
				else:
						print str(best)+'-'+str(i),
	print ''
