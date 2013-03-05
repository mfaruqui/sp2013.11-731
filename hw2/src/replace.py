import sys

for line in sys.stdin:
	line = line.strip()
	lines = line.split(' | | | ')
	for line in lines:
		print line
