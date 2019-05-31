import os

import HuffmanEncoder as H


inputFileName = "test.txt"
outFileName = "test.bin"
decompressFileName = "decompress.txt"

encoder = H.HuffmanEncoder(inputFileName)
encoder.compress(outFileName)
encoder.decode(outFileName,decompressFileName)

print("before encoding size", os.stat(inputFileName).st_size)
print("after encoding size", os.stat(outFileName).st_size)