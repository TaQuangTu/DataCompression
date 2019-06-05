import os


class LzwEncoder:
    def __init__(self):
        self.mDict = {}
        self.reverseDict = {}

    def __initDict(self, text):
        self.mDict = {}
        for char in text:
            if not char in self.mDict:
                self.mDict[char] = len(self.mDict) + 1
                self.reverseDict[len(self.mDict)] = char

    def __getEncodeByteArray(self, text):
        intArray = []
        self.__initDict(text)
        s = text[0]
        for char in text[1:]:
            if not (s + char) in self.mDict:
                self.mDict[s + char] = len(self.mDict) + 1
                intArray.append(self.mDict[s])
                s = char
            else:
                s = s + char
        intArray.append(self.mDict[s])
        bytes = bytearray(intArray)
        return bytes

    def compress(self, inputFilePath, outputFilePath):
        with open(inputFilePath, "r+") as inputFile, open(outputFilePath, "wb") as outputFile:
            text = inputFile.read()
            text = text.rstrip()
            bytearray = self.__getEncodeByteArray(text)
            for item in bytearray:
                print(item)
            outputFile.write(bytearray)

    def decompress(self, decompressFilePath, outputFilePath):

        with open(decompressFilePath, 'rb') as dFile, open(outputFilePath, 'w') as oFile:
            resultText = ""
            s = "NIL"
            bytes = dFile.read(1)
            while (bytes != "" and len(bytes) != 0):
                print("4 bytes = ", bytes)
                k = int.from_bytes(bytes,"little")
                print("k ",k)
                entry = self.reverseDict[k]
                resultText += entry
                if s != "NIL":
                    self.reverseDict[len(self.reverseDict)+1] = s+entry[0]
                s = entry
                bytes = dFile.read(1)
            print("decode = ", resultText)
