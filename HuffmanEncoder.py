import functools
import os
import heapq


@functools.total_ordering
class HuffmanNode:
    def __init__(self, char, frequency):
        self.mChar = char
        self.mFrequency = frequency
        self.mLeft = None
        self.mRight = None

    def __cmp__(self, other):
        if (other == None):
            return -1
        if (not isinstance(other, HuffmanNode)):
            return -1
        return other.mFrequency > other.mFrequency

    def __lt__(self, other):
        if (other == None):
            return -1
        if (not isinstance(other, HuffmanNode)):
            return -1
        return other.mFrequency < other.mFrequency


class HuffmanEncoder:
    def __init__(self, filePath):
        self.mFilePath = filePath
        self.mHeap = []
        self.mCodes = {}
        self.mReverseCodes = {}

    # helper methods
    def __makeFrequencyDict(self, text):
        frequencesDict = {}
        for char in text:
            if not char in frequencesDict:
                frequencesDict[char] = 0
            else:
                frequencesDict[char] += 1

        print("Frequency: ", frequencesDict)
        return frequencesDict

    def __makeHeap(self, frequency):
        for key in frequency:
            node = HuffmanNode(key, frequency[key])
            heapq.heappush(self.mHeap, node)

    def __mergeNodes(self):
        while len(self.mHeap) > 1:
            print("heaplen= ", len(self.mHeap))
            node1 = heapq.heappop(self.mHeap)
            node2 = heapq.heappop(self.mHeap)
            print("node1 = ", node1.mChar, ",", node1.mFrequency)
            print("node2 = ", node2.mChar, ",", node2.mFrequency)
            mergedNode = HuffmanNode(None, node1.mFrequency + node2.mFrequency)
            mergedNode.mLeft = node1
            mergedNode.mRight = node2
            heapq.heappush(self.mHeap, mergedNode)

    def __makeCodes(self, currentNode, currentCode):
        if currentNode is None:
            return
        if currentNode.mChar != None:
            self.mCodes[currentNode.mChar] = currentCode
            self.mReverseCodes[currentCode] = currentNode.mChar
            print(self.mCodes)
            print(self.mReverseCodes)
        else:
            self.__makeCodes(currentNode.mLeft, currentCode + "0")
            self.__makeCodes(currentNode.mRight, currentCode + "1")

    def __encode(self, text):
        encodedText = ""
        for char in text:
            encodedText += self.mCodes[char]
        # padding if need
        paddingBits = 8 - (len(encodedText) % 8)

        for i in range(paddingBits):
            encodedText += "0"
        paddingInfo = "{0:08b}".format(paddingBits)
        encodedText = paddingInfo + encodedText
        return encodedText

    def __getEncodedByte(self, encodedText):
        b = bytearray()
        for i in range(0, len(encodedText), 8):
            byte = encodedText[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, outFilePath):
        with open(self.mFilePath, "r+") as file, open(outFilePath, "wb") as output:
            text = file.read()
            text = text.rstrip()
            frequencyDict = self.__makeFrequencyDict(text)
            self.__makeHeap(frequencyDict)
            self.__mergeNodes()
            self.__makeCodes(self.mHeap[0], "")
            encodedText = self.__encode(text)
            b = self.__getEncodedByte(encodedText)
            output.write(bytes(b))

    def __removePadding(self, encodedText):
        paddedInfo = encodedText[0:8]
        paddingBits = int(paddedInfo, 2)
        paddedEncodeText = encodedText[8:]
        encodedText = paddedEncodeText[:-paddingBits]
        return encodedText

    def decode(self, encodeFileName, decodeFileName):
        with open(encodeFileName, 'rb') as file, open(decodeFileName, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while (byte != "" and len(byte) != 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            encodeText = self.__removePadding(bit_string)

            decompressText = ""
            word = ""
            for char in encodeText:
                word = word + char
                if word in self.mReverseCodes:
                    decompressText += self.mReverseCodes[word]
                    word = ""
            output.write(decompressText)
