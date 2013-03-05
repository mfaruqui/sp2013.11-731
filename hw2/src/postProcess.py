import sys 

for line in sys.stdin:
    line = line.strip()
    val = float(line)

    if val >= 0.5:
       print 1
    elif val < 0.5 and val >= 0:
       print 0
    elif val > -0.5 and val < 0:
	    print 0
    else:
	    print -1
      
       
