def BWT(s):
    N = len(s)
    compressed = bytearray()
    BWM = [s[i:] + s[0:i] for i in range(N)]
    BWM.sort()
    for i in range(N):
        compressed.append(BWM[i][-1])
    S_index = BWM.index(s)
    return bytes(compressed), S_index

def iBWT(compressed,s_ind):
    N = len(compressed)
    new_s = bytearray()
    BWM = ["" for _ in range(N)]
    for _ in range(N):
        for j in range(N):
            BWM[j] = chr(compressed[j]) + BWM[j]
        BWM.sort()
    S = BWM[s_ind]
    return S


string = b'abracadabra' + b'$'
print(string)
print(BWT(string))
col, s_ind =(BWT(string))
print(iBWT(col, s_ind))