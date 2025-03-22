def bMTF(S):
    T = [chr(i) for i in range(128)]
    L = []
    s_new = bytearray()
    for s in S:
        i = T.index(chr(s))
        L.append(i)
        s_new.append(i)
        T = [T[i]] + T[:i] + T[i+1:]
    return bytes(s_new)

def ibMTF(S):
    T = [chr(i) for i in range(128)]
    S_new = bytearray()
    for s in S:
        char = chr(s)
        i = T.index(char)
        S_new.append(s)
        T.insert(0, T.pop(i))
    return bytes(S_new)

s = b'aaaaaaabbbbbbbcccccccccccdefrt'
print(s)
print(repr(bMTF(s)))
print(ibMTF(s))
