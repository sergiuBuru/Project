# imports
from hashlib import sha256 as sha
from binascii import hexlify, unhexlify
from time import time
from struct import pack, unpack

# hash function
# takes in a string
# returns a SHA-256 encoded hex-string


def hashSHA(string):
    return hexlify(sha(string.encode()).digest()).decode()

# create block
# takes in hash of previous block
# returns a dictionary object with:
# hash of previous block, data field, and the newly created block's hash


def createBlock(data, prevHash):
    blockHash = hashSHA(prevHash + data)
    return {
        'prevHash': prevHash,
        'data': data,
        'blockHash': blockHash
    }

# is valid
# takes in two blocks
# checks to see if the second block's previous hash field
# is equivalent to the first block's hash field


def isValid(blockA, blockB):
    return blockB['prevHash'] == blockA['blockHash']

# blockchain class
# contains the actual list of blocks and
# corresponding operations


class Blockchain:

    def __init__(self):
        self.chain = []

    # add block
    # takes in a block
    # adds it to the end of the chain
    def addBlock(self, block):
        self.chain.append(block)

    # top
    # returns the last block in the chain
    def top(self):
        return self.chain[-1]

    # height
    # returns the height (length) of the chain
    def height(self):
        return len(self.chain)

# genesis
# creates a block, but uses a null hash as the previous hash


def genesis():
    prevHash = "0"*64
    data = "genesis"
    return createBlock(data, prevHash)

# to integer
# takes in a byte string as an argument
# returns an integer with big endian byte order


def toInt(bytestring):
    return int.from_bytes(unhexlify(bytestring), byteorder='big')

# proof of work
# takes in data, a previous hash, and a target
# works to calculate a hash integer value less than the target
# does this by "incremental guessing"
# timestamp and nonce update each time we "swing the pick axe"
# once it's found, the output is like a traditional block
# but with the new fields as well


def createBlockPoW(data, prevHash, target):
    nonce = 0
    timestamp = int(time())
    blockHash = hashSHA(prevHash + data + str(timestamp) +
                        str(target) + str(nonce))
    while not toInt(blockHash) < target:
        nonce += 1
        timestamp = int(time())
        blockHash = hashSHA(prevHash + data + str(timestamp) +
                            str(target) + str(nonce))
    return {
        'prevHash': prevHash,
        'data': data,
        'timestamp': timestamp,
        'target': target,
        'nonce': nonce,
        'blockHash': blockHash
    }

############################################################################
############################ NEW CODE BELOW HERE ###########################
############################################################################

def hash_SHA(byte_string): 
    return hexlify(sha(byte_string).digest())

def time_now():
    """
    This function takes the current time and returns it as an integer

    :returns: an integer, representing the current system time.
    """
    return int(time())

def less_than_target(byte_string, target):
    """
    This funciton determines which of a byte string holding an integer, or a target integer is lesser.

    :param1 byte_string: a byte string intended to hold an integer
    :param2 targer: an integer, a target to which byte_string is compared  
    :returns: a boolean, true if the byte_string integer is less than target. false otherwise
    """
    out = False
    if (toInt(byte_string) < target):
        out = True
    return out

def bytes_to_int(byte_string):
    """
    This function intends to convert a four byte string into an unsinged integer

    :param1 byte_string: a byte string, assumed to be four bytes, holding an integer
    :returns: an unsinged integer, drawn from byte_string
    """
    return unpack('I', byte_string)[0]

def bytes_to_short(byte_string):
    """
    This function intends to convert a four byte string into an unsigned short integer

    :param1 byte_string: a byte string, assumed to be four bytes, holding an integer
    :returns: an unsinged short integer, drawn from byte_string
    """
    return unpack('H', byte_string)[0]

def bytes_to_long(byte_string):
    """
    This function intends to convert a four byte string into an unsigned long integer

    :param1 byte_string: a byte string, assumed to be four bytes, holding an integer
    :returns: an unigned long integer, drawn from byte_string
    """
    return unpack('L', byte_string)[0]
