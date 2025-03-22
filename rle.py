def RLE(s):
    compressed = bytearray()
    flag = False
    counter = 1
    prev_symb = s[0]
    for symb in s[1:]:
        if prev_symb == symb:
            if flag == True:
                compressed.append(ord(b'#'))
                flag = False
            counter += 1
        else:
            if counter == 1:
                if flag == False:
                    compressed.append(ord(b'#'))
                    flag = True
                compressed.append(prev_symb)
            else:
                compressed.append(counter)
                compressed.append(prev_symb)
                counter = 1
        prev_symb = symb
    if flag == True:
        compressed.append(ord(b'#'))
    return bytes(compressed)

def iRLE(compressed):
    s = bytearray()
    N = len(compressed)
    i = 0
    while(i < N):
        if compressed[i] != ord(b"#"):
            lenght = compressed[i]
            symb = compressed[i+1]
            for j in range(lenght):
                s.append(symb)
            i += 2
        else:
            i += 1
            while( i < N and compressed[i] != ord(b"#")):
                s.append(compressed[i])
                i += 1
            i += 1
    return bytes(s)


string = b'aaaacdfcdfcdfrrrrrrrrr' + b'$'
print(string)
print(RLE(string))
print(iRLE(RLE(string)))
