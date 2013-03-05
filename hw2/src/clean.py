import sys

for line in sys.stdin:
    
    line = line.strip()
    line = line.replace("&quot;",'"')
    line = line.replace("&#39;","'")
    
    print line.lower()