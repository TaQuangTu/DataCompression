import os

from EncodingAlgorithms import HuffmanEncoder as H
from EncodingAlgorithms import LZWEncoder as L

# inputFileName = "test.txt"
# outFileName = "test.bin"
# decompressFileName = "decompress.txt"
#
# encoder = H.HuffmanEncoder(inputFileName)
# encoder.compress(outFileName)
# encoder.decompress(outFileName, decompressFileName)
#
# print("before encoding size", os.stat(inputFileName).st_size)
# print("after encoding size", os.stat(outFileName).st_size)

lzwEncoder = L.LzwEncoder()
lzwEncoder.compress("test.txt","testlzw.bin")
lzwEncoder.decompress("testlzw.bin","decompress.txt")