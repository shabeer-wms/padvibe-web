import re,sys
t=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'marketing','ads.md')).read()
h=re.search(r"Headlines.*?\n\n((?:\d+\. .*\n)+)",t).group(1)
d=re.search(r"Descriptions.*?\n\n((?:\d+\. .*\n)+)",t).group(1)
bad=0
for line in h.strip().split("\n"):
    s=line.split(". ",1)[1]
    if len(s)>30: print("HEADLINE too long",len(s),s); bad+=1
for line in d.strip().split("\n"):
    s=line.split(". ",1)[1]
    if len(s)>90: print("DESC too long",len(s),s); bad+=1
print("headlines",len(h.strip().split("\n")),"descriptions",len(d.strip().split("\n")),"problems",bad)
