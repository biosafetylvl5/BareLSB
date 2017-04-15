import hashlib


class Oversize(Exception):
    pass


class HashMismatch(Exception):
    pass


class BareLSB:
    def __init__(self, img):
        self.pos = self.updatePosition()
        self.image = img
        self.end = "$%bar%$"
        self.maximumCapacity = self.determineMaximumCapacity(dim(self.image))

    @staticmethod
    def getLSB(byte):
        return byte & 1 == 1

    def setLSB(self, value, byte):
        """
        :type value: int
        :type byte: int
        """
        if not self.getLSB(byte):
            return value & 0b11111110  # to change to 0
        else:
            return value | 0b1  # change to 1

    def determineMaximumCapacity(self, imgDim):
        capacity = 1
        for x in imgDim:
            capacity = capacity * x
        return capacity - 256 - len(strToByteArray(self.end) * 8)

    def getPixel(self, position):
        return self.image[position[0]][position[1]][position[2]]

    def setPixel(self, position, value):
        self.image[position[0]][position[1]][position[2]] = value

    def updatePosition(self):
        dimension = dim(self.image)
        for x in range(dimension[0]):
            for y in range(dimension[1]):
                for z in range(dimension[2]):
                    yield (x, y, z)

    def addStr(self, string):
        return self.addBin(strToByteArray(string))

    def addBin(self, bytes):
        """
        :type bytes: List[int]
        """
        if self.maximumCapacity < len(bytes) * 8:
            raise Oversize("Data to large to fit into LSB of image provided")
        checksum = hashlib.sha256()
        for byte in bytes:
            self.addByte(byte)
            checksum.update(bin(byte).replace('0b', '').zfill(8))
        for byte in bytearray(checksum.hexdigest(), 'utf-8'):  # add checksum
            self.addByte(byte)
        for byte in bytearray(self.end, 'ascii'):
            self.addByte(byte)

    @property
    def getEnd(self):
        string_end_binary = ""
        for byte in bytearray(self.end, 'ascii'):
            for x in bin(byte).replace('0b', '').zfill(8):  # TODO: Not very pythonic, probably a better way
                string_end_binary += x
        return string_end_binary

    def addByte(self, byte):
        for x in bin(byte).replace('0b', '').zfill(8):  # TODO: Not very pythonic, probably a better way
            self.addBit(int(x))

    def addBit(self, bit):
        pos = self.pos.next()
        pixel = self.getPixel(pos)
        pixel = self.setLSB(pixel, bit)
        self.setPixel(pos, pixel)

    def readBit(self, pos):
        return self.getLSB(self.getPixel(pos))

    def getBin(self, ignoreHash=False):
        dimension = dim(self.image)
        end = self.getEnd
        msg = ""
        for x in range(dimension[0]):
            for y in range(dimension[1]):
                for z in range(dimension[2]):
                    msg += str(int(self.readBit((x, y, z))))
                    if end in msg:
                        result = msg.replace(end, '')
                        checksum = result[len(result) - 512:]
                        content = result[:len(result) - 512]
                        if (not ignoreHash) and (not getHashBin(content) == checksum):
                            raise HashMismatch(
                                "Content does not match checksum, use ignoreHash=True to disable checksum checking")
                        return content, checksum

    def getText(self):
        binary = self.getBin()
        message = ""
        for x in range(0, len(binary[0]) / 8):
            message += chr(int(binary[0][x * 8:(x + 1) * 8], 2))
        return message


def getHashBin(data):
    checksum = ""
    for byte in bytearray(hashlib.sha256(data).hexdigest(), 'utf-8'):
        for bit in bin(byte).replace('0b', '').zfill(8):
            checksum += str(bit)
    return checksum


def strToByteArray(string):
    byte_array = bytearray()
    byte_array.extend(string)
    return [int('0b' + bin(x).replace('0b', '').zfill(8), 2) for x in byte_array]


def dim(img):
    return img.shape
