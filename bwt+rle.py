import os
from bwt import BWT, iBWT
from rle import RLE, iRLE
from mtf import MTF, iMTF
from ha import HA, iHA
from lz78 import LZ78, iLZ78
from lz77 import LZ77, iLZ77

def bytes_to_dict(byte_string: bytes) -> dict:
    result = {}
    seen_bytes = set()

    for byte in byte_string:
        if byte not in seen_bytes:
            index = len(seen_bytes)
            binary_representation = format(index, '08b')
            result[byte] = binary_representation
            seen_bytes.add(byte)

    return result



if __name__ == "__main__":

##    with open('compressed1.txt', 'w'):
##        pass

##    with open('decompressed.txt', 'w'):
##        pass

##    with open('tsvet.raw', 'rb') as IF, open('compressed1.txt', 'wb+') as CF:
##        while True:
##            block = IF.read(10000)
##            if not block:
##                break
##            compressed_block1, ind = BWT(block)
##            Ind.append(ind)
####            compressed_block2 = MTF(compressed_block1)
####            compressed_block3 = RLE(compressed_block2)
####            compressed_block4, huf = HA(compressed_block3)
##            CF.write(bytes(ind)+b'\n')
##            CF.write(compressed_block1)
####        print((os.path.getsize('compressed.txt')/os.path.getsize('bin.exe')))
####        print(f"Размер оригинального файла: {os.path.getsize('bin.exe')} байт")
####        print(f"Размер сжатого файла: {os.path.getsize('compressed1.txt')} байт")

    with open('tsvet.raw', 'rb') as NF, open('compressed2.txt', 'wb+') as FCF:
        while True:
            block = NF.read()
            if not block:
                break
            #compressed_block1 = BWT(block)
            compressed_block2 = MTF(block)
##            compressed_block3 = RLE(compressed_block2)
            compressed_block4, huf = HA(compressed_block2)
            FCF.write(bytes(huf)+b'\n')
            FCF.write(compressed_block4)
##        print((os.path.getsize('tsvet.raw')/os.path.getsize('compressed2.txt')))
##        print(f"Размер оригинального файла: {os.path.getsize('compressed2.txt')} байт")
##        print(f"Размер сжатого файла: {os.path.getsize('compressed2.txt')} байт")

    with open('compressed2.txt', 'rb') as FCF, open('decompressed1.raw', 'wb+') as FDF:
        while True:
            bhufc = FCF.readline()
            bhufc += FCF.readline()
            hufc = bytes_to_dict(bhufc)
            block = FCF.read()
            if not block:
                break
            #compressed_block1 = BWT(block)
            compressed_block41 = iHA(block, hufc)
##            compressed_block31 = iRLE(compressed_block41)
            compressed_block21 = iMTF(compressed_block41)
            FDF.write(compressed_block21)
##        print((os.path.getsize('grey.raw')/os.path.getsize('compressed2.txt')))
##        print(f"Размер оригинального файла: {os.path.getsize('tsvet.raw')} байт")
##        print(f"Размер сжатого файла: {os.path.getsize('compressed2.txt')} байт")

##    with open('decompressed1.txt', 'rb') as FCF, open('decompressed2.raw', 'wb+') as FDF:
##        while True:
##            ind = len(FCF.readline())-1
##            block = FCF.read(10000)
##            if not block:
##                break
##            compressed_block11 = iBWT(block, ind)
####            compressed_block4 = iHA(block, huf)
####            compressed_block3 = iRLE(compressed_block4)
####            compressed_block2 = iMTF(compressed_block3)
##            FDF.write(compressed_block11)
########        print((os.path.getsize('decompressed2.txt')/os.path.getsize('text.txt')))
######        print(f"Размер оригинального файла: {os.path.getsize('RUcomLZ77.txt')} байт")
######        print(f"Размер сжатого файла: {os.path.getsize('TcomLZ77.txt')} байт")
####
##
##with open('bin.exe', 'rb') as IF, open('compressed1.txt', 'wb+') as CF:
####        while True:
##    block = IF.read()
####            if not block:
####                break
####            compressed_block1, ind = BWT(block)
##    CF.write(block)
