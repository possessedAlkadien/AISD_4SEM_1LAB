import os

def RLE(s: bytes) -> bytes:
    if not s:
        return b''

    marker = 0xFF  # Используем байт 255 как маркер
    compressed = bytearray()
    counter = 1
    prev_symb = s[0]
    FLag = False

    for symb in s[1:]:
        if prev_symb == symb:
            if FLag == True:
                compressed.append(marker)
                FLag = False
            counter += 1
        else:
            # Обработка предыдущей последовательности
            if counter > 1:
                while counter >= 255:
                    compressed.append(254)
                    compressed.append(prev_symb)
                    counter -= 254
                compressed.append(counter)
                compressed.append(prev_symb)
                counter = 1
            else:
                if FLag == False:
                    compressed.append(marker)
                    FLag = True
                compressed.append(prev_symb)

            prev_symb = symb

    if FLag == True:
        compressed.append(marker)

    return bytes(compressed)

def iRLE(compressed: bytes) -> bytes:
    marker = 0xFF
    s = bytearray()
    i = 0
    N = len(compressed)

    while i < N:
        if compressed[i] == marker:
            i += 1
            while i < N and compressed[i] != marker:
                s.append(compressed[i])
                i += 1
            i += 1
        else:
            length = compressed[i]
            symb = compressed[i + 1]
            s.extend([symb] * length)
            i += 2

    return bytes(s)
