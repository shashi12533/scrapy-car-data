


def repeated(s):
    a = 2**32
    for i in s:
        p  = ord(i)-97
        h = bin(a)[2:]
        if h[-(p+1)]=="0":
            a = a | (1 << p)
        else:
            print(s.index(i)-1)
            break
    # a = a | (1<<2)


















s = "loveleetcode"
repeated(s)