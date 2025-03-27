def RLE(s: bytes) -> bytes:
    if not s:
        return b''

    compressed = bytearray()
    counter = 1
    Ncounter = 0
    prev_symb = s[0]
    flag = False
    Nep = []

    for symb in s[1:]:
        if prev_symb == symb:
            if flag == True:
                while Ncounter > 127:
                    compressed.append(127 | 0x80)
                    for i in Nep[:127]:
                        compressed.append(i)
                    Ncounter -= 127
                    Nep = Nep[127:]
                compressed.append(Ncounter | 0x80)
                for i in Nep:
                    compressed.append(i)
                flag = False
                Nep = []
                Ncounter = 0
            counter += 1
        else:
            if counter > 1:
                while counter>127:
                    compressed.append(127 & 0x7F)
                    compressed.append(prev_symb)
                    counter -= 127
                compressed.append(counter & 0x7F)
                compressed.append(prev_symb)
                counter = 1
            else:
                if flag == False:
                    flag = True
                Ncounter += 1
                Nep.append(prev_symb)
            prev_symb = symb


    if counter > 1:
        compressed.append(counter & 0x7F)
        compressed.append(prev_symb)
    else:
        compressed.append((1 << 7) | 1)
        compressed.append(prev_symb)

    return bytes(compressed)

def iRLE(compressed: bytes) -> bytes:
    s = bytearray()
    i = 0
    N = len(compressed)

    while i < N:
        count = compressed[i]
        if count & 0x80:
            count = count & 0x7F
            while count > 0:
                s.append(compressed[i + 1])
                count-=1
                i+=1
            i += 1
        else:
            symb = compressed[i + 1]
            s.extend([symb] * count)
            i += 2

    return bytes(s)

##s = b'esjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhcebesjbckseucakhceeb'
##print(RLE(s))
##print(iRLE(RLE(s)))