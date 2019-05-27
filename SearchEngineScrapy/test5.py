

def permute(n,s):
    if len(s)>n:
        return
    if len(s)==n:
        if s.count("b")<=1 and s.count("c")<=2:
           l.append(s)
           return


    for i in ("a","b","c"):
        permute(n,s+i)


n=3
s=""
l=[]
permute(n,s)
print(len(l),l)