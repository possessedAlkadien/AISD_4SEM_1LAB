import os

def MTF(S):
    T = [chr(i) for i in range(512)]
    s_new = bytearray()
    for s in S:
        i = T.index(chr(s))
        s_new.append(i)

        T.insert(0, T.pop(i))
    return bytes(s_new)

def iMTF(S):
    T = [chr(i) for i in range(512)]
    S_new = bytearray()
    for s in S:
        # Получаем индекс символа
        i = s
        S_new.append(ord(T[i]))
        T.insert(0, T.pop(i))
    return bytes(S_new)

