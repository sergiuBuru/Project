# imports
from hashlib import sha256 as sha
from binascii import hexlify, unhexlify
from time import time
from struct import pack, unpack
import math

# hash function
# takes in a string
# returns a SHA-256 encoded hex-string


def hashSHA(string):
    """
    Hashes the inputed string using SHA256 from the hash Library

    :param string: The string that is going to be hashed
    :return: The inputed string as a hash
    """

    return hexlify(sha(string.encode()).digest()).decode()

# create block
# takes in hash of previous block
# returns a dictionary object with:
# hash of previous block, data field, and the newly created block's hash


def createBlock(data, prevHash):
    """
    Creates a new block into the chain

    :param data: Data being stored in   (a string)
    :param prevHash: Hash to previous block in the chain    (a string)
    :return: A dictionary containing the hash to the previous block,
                data it was given, and the new blocks hash.
    """

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
    """
    Takes in two given blocks and checks if they are consequtive blocks in the chain

    :param blockA: Block that comes first in the chain so to say.
                    Block closet to the Genesis block.
    :param blockB: Block that comes second out of the 2 blocks.
                    Block closest to the top of the chain.
    :return: True or False
    """

    return blockB['prevHash'] == blockA['blockHash']

# blockchain class
# contains the actual list of blocks and
# corresponding operations


class Blockchain:

    def __init__(self):
        """
        Constructor of the Blockchain class

        :no parameter:
        :no return:
        """

        self.chain = []

    # add block
    # takes in a block
    # adds it to the end of the chain
    def addBlock(self, block):
        """
        Adds a block to the top of the chain

        :param self: The whole blockchain itself
        :param block: The newly added block
        :no return:
        """

        self.chain.append(block)

    # top
    # returns the last block in the chain
    def top(self):
        """
        Gets the top block from the chain

        :param self: The whole blockchain itself
        :return: The block at the last index in the chain
        """

        return self.chain[-1]

    # height
    # returns the height (length) of the chain
    def height(self):
        """
        Gives the total size of the blockchain

        :param self: The whole blockchain itself
        :return: The number of current blocks in the chain (integer)
        """

        return len(self.chain)

# genesis
# creates a block, but uses a null hash as the previous hash


def genesis():
    """
    Creates the Genesis block in the blockchain (first block in the chain)

    :no parameter:
    :return: The hash to this block and the data this block contains    (both strings)
    """

    prevHash = "0"*64
    data = "genesis"
    return createBlock(data, prevHash)

# to integer
# takes in a byte string as an argument
# returns an integer with big endian byte order


def toInt(bytestring):
    """
    Converts the inputed byte string in big endian to an integer

    :param bytestring: A byte string in big endian byte order
    :return: Integer format of inputed byte string
    """

    return int.from_bytes(unhexlify(bytestring), byteorder='big')

# proof of work
# takes in data, a previous hash, and a target
# works to calculate a hash integer value less than the target
# does this by "incremental guessing"
# timestamp and nonce update each time we "swing the pick axe"
# once it's found, the output is like a traditional block
# but with the new fields as well


def createBlockPoW(data, prevHash, target):
    """
    The nounce, timestamp, and target hash are converted into strings, they are then
    added with the previous hash and the data then hashed together creating a unique hash.
    A blocks proof of work is made through hashing until the created hash is less than
    (close enough) to the target hash.

    :param data: Actual data being stored into the block (a string)
    :param prevHash: The hash to the previous block in the chain (a string)
    :param target: The hash the while loop will try to approach after
                    rehashing the incremented nonce and getting the current time.
    :return: A dictionary containing the hash to previous block, data stored, time stamp, target hash
                used, the nonce used to produce the new blocks' hash, and the hash to the newly created block.
    """

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
    """
    Hashes the inputed byte string using SHA256 from the hash Library

    :param byte_string: The byte string that is going to be hashed
    :return: The hash of the inputed byte string
    """

    return hexlify(sha(byte_string).digest())
    


def int_to_bytes(val):
    """
    Given an integer i, return it in byte form, as an unsiged int 
    Will only work for positive ints. 
    Max value accepted is 2^32 - 1 or 4,294,967,295
    Basically any valid positive 32 bit int will work 
    
    :param val: integer i 
    :return: integer i in byte form as unsigned int.
    """
    return pack('I', val)

def short_to_bytes(val):
    """
    Given an short i, return it in byte form, as an unsiged short 
    Will only work for positive shorts. 
    Max value accepted is 2^8 - 1 or 65535
    Basically any valid positive 8 bit int will work 
    
    :param val: short i 
    :return: short i in byte form as unsigned short.
    """
    return pack('H', val)

def long_to_bytes(val):
    """
    Given an long i, return it in byte form, as an unsiged long 
    Will only work for positive longs. 
    Max value accepted is 2^32 - 1 or 4,294,967,295
    Basically any valid positive 8 bit int will work 
    
    :param val: long i 
    :return: long i in byte form as unsigned long.
    """
    return pack('L', val)

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
    return toInt(byte_string) < target

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


def log_target_bytes(base10_number):
    """
    Converts the unsigned log base 10 of the inputed number into bytes

    :param base10_number: A number of base 10
    :return: The log base 10 of the unputed number as bytes
    """
    return short_to_bytes(int(math.log10(base10_number)))