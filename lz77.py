def LZ77(S):
    buffer_size = 10
    string_size = 10
    coding_list = []
    buffer = ""
    N = len(S)
    i = 0
    while i < N:
        buffer = S[max(0,i-buffer_size) : i]
        new_buffer_size = len(buffer)
        shift = -1
        for j in range(string_size, -1, -1):
            subS = S[i : min(i + j,N)]
            shift = buffer.find(subS)
            if shift != -1:
                break
        coding_list.append((new_buffer_size - shift, len(subS), chr(S[i + len(subS)])))
        i += len(subS)+1
    return coding_list

# декодирование LZ77
def iLZ77(compressed_message):
    S = bytearray()
    for t in compressed_message:
        shift, length, symbol = t
        N =len(S)
        S.extend(S[N-shift : N-shift+length])
        S.append(ord(symbol))
    return bytes(S)

string = b'aaaaaaaaabbbbbefdsgtttttt' + b'$'
print(LZ77(string))
print(iLZ77(LZ77(string)))
print((string+b'$')==iLZ77(LZ77(string)))