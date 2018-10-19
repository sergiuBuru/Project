# imports
import unittest
from block import *
import time
from struct import unpack

# unit test class


class TestBlock(unittest.TestCase):

    # test hash function

    def testHashSHA(self):
        # testHashSHA part 1:
        # take two different strings
        # check to see if hashes are different
        a = "apple"
        b = "orange"
        hashA = hashSHA(a)
        hashB = hashSHA(b)
        self.assertNotEqual(hashA, hashB)

        # testHashSHA part 2:
        # take two long strings with a single letter changed
        # check to see if hashes are different
        s1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        s2 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minin veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        hashS1 = hashSHA(s1)
        hashS2 = hashSHA(s2)
        self.assertNotEqual(hashS1, hashS2)

        # testHashSHA part 3:
        # take two of the same strings
        # hash them separately
        # check to see if the hashes are equivalent
        c = "melon"
        d = "melon"
        hashC = hashSHA(c)
        hashD = hashSHA(d)
        self.assertEqual(hashC, hashD)

    # test is valid
    # check to see if a block points backwards to a previous block
    def testIsValid(self):
        blockA = createBlock('this is block a', '000')
        blockB = createBlock('this is block b', blockA['blockHash'])
        self.assertTrue(isValid(blockA, blockB))

    # test add block
    # check to see if when adding a block it is contained in the chain
    def testAddBlock(self):
        bc = Blockchain()
        testBlock = createBlock('this is a test', '123456789')
        bc.addBlock(testBlock)
        self.assertEqual(bc.chain[0], testBlock)

    # test top
    # check to see if calling top returns the last block in the chain

    def testTop(self):
        bc = Blockchain()
        testBlock = createBlock('this is a test', '123456789')
        bc.addBlock(testBlock)
        self.assertEqual(bc.top(), testBlock)

    # test height
    # check to see if height returns the length of the chain
    def testHeight(self):
        bc = Blockchain()
        testBlock = createBlock('this is a test', '123456789')
        bc.addBlock(testBlock)
        bc.addBlock(testBlock)
        bc.addBlock(testBlock)
        bc.addBlock(testBlock)
        self.assertEqual(4, bc.height())

    # test proof of work
    # check to see if a proof of work mined block
    # contains a hash that's less than the target
    # check also how much time it takes to mine a block
    def testPoW(self):
        data = 'testPoW'
        prevHash = '000000'
        # play around with this exponent (stick to the 60-100 range)
        target = 10**75
        print("Mining...")
        a = int(time.time())
        b = createBlockPoW(data, prevHash, target)
        print("Block found!")
        c = int(time.time())
        print("Time it took: {} seconds".format((c-a)))
        self.assertLessEqual(toInt(b['blockHash']), target)

    def test_Hash_SHA(self):
        data = "SIG Blockchain"
        actual = hash_SHA(data.encode())
        self.assertIsInstance(actual, bytes)

    def test_int_to_bytes(self):
        """
        Tests out values for the int_to_bytes function. Tests out max values as well
        """
        byte1 = int_to_bytes(1) 
        #if we unpack the bytes as a unsigned integer, we should get the same value
        self.assertEqual(unpack('I', byte1)[0], 1)
        #test out 0
        byte0 = int_to_bytes(0) 
        self.assertEqual(unpack('I', byte0)[0], 0)
        #test out max signed 32 bit int
        byte_max_32 = int_to_bytes(2**31 -1)
        self.assertEqual(unpack('I', byte_max_32)[0], 2**31 -1)
        #test out max unsigned 32 bit int 
        byte_max_u32 = int_to_bytes(2**32 -1)
        self.assertEqual(unpack('I', byte_max_u32)[0], 2**32 -1)
     
    def test_short_to_bytes(self):
        """
        Tests out values for the short_to_bytes function. Tests out max values as well
        """
        byte1 = short_to_bytes(1) 
        #if we unpack the bytes as a unsigned integer, we should get the same value
        self.assertEqual(unpack('H', byte1)[0], 1)
        #test out 0
        byte0 = short_to_bytes(0) 
        self.assertEqual(unpack('H', byte0)[0], 0)
        #test out max unsigned 32 bit int 
        byte_max_short = short_to_bytes(2**8 -1)
        self.assertEqual(unpack('H', byte_max_short)[0], 2**8 -1)
       
    def test_long_to_bytes(self):
        """
        Tests out values for the long_to_bytes function. Tests out max values as well
        """
        byte1 = long_to_bytes(1) 
        #if we unpack the bytes as a unsigned integer, we should get the same value
        self.assertEqual(unpack('L', byte1)[0], 1)
        #test out 0
        byte0 = long_to_bytes(0) 
        self.assertEqual(unpack('L', byte0)[0], 0)
        #test out max unsigned 32 bit int 
        byte_max_long = long_to_bytes(2**32 -1)
        self.assertEqual(unpack('L', byte_max_long)[0], 2**32 -1)

    # Tests time_now() by printing the current time, converting it
    # to an int manually, and comparing it to the output of time_now
    def test_time_now(self):
        curr_time = time.time()
        print("Float Time: " + str(curr_time))
        int_time = int(curr_time)
        print("Integer Time:  " + str(time_now()))
        self.assertEqual(int_time, time_now())

    # Converts a known value to a bytestring and manually converts to string
    # Compares to output of less_than_target with known greater value
    def test_less_than_target(self):
        target = 30
        test_bs = hexlify(bytes([20]))
        print("Target: " + str(target))
        print("From Byte: " + str(toInt(test_bs)))
        self.assertTrue(less_than_target(test_bs, target))

    # Converts a known value to a byte string, manually converts it back into an
    # integer, compares this integer to the output of bytes_to_int()
    def test_bytes_to_int(self):
        convert = 20
        byte_s = pack('I', convert)
        print("Byte String: " + str(convert))
        print("Expected Result: " + str(convert))
        print("Result: " + str(bytes_to_int(byte_s)))
        self.assertEqual(convert, bytes_to_int(byte_s))

    # Converts a known value to a byte string, manually converts it back into an
    # integer, compares this integer to the output of bytes_to_int()
    def test_bytes_to_short(self):
        convert = 30
        byte_s = pack('H', convert)
        print("Byte String: " + str(convert))
        print("Expected Result: " + str(convert))
        print("Result: " + str(bytes_to_short(byte_s)))
        self.assertEqual(convert, bytes_to_short(byte_s))

    # Converts a known value to a byte string, manually converts it back into an
    # integer, compares this integer to the output of bytes_to_int()
    def test_bytes_to_long(self):
        convert = 40
        byte_s = pack('L', convert)
        print("Byte String: " + str(convert))
        print("Expected Result: " + str(convert))
        print("Result: " + str(bytes_to_long(byte_s)))
        self.assertEqual(convert, bytes_to_long(byte_s))

    # Gets the log of a given whole number of base 10 and converts it into bytes
    # Uses short_to_bytes function for byte conversion
    def test_log_target_bytes(self):
        convert = 10000             #10^4
        byte_form = log_target_bytes(convert)
        print("Converting: ", convert, " Written as: 10^4")
        print("Bytes using function: ", byte_form)
        print("Reverting to get log: ", int.from_bytes(byte_form,byteorder = 'little'))
        self.assertEqual(convert, pow(10,int.from_bytes(byte_form,byteorder = 'little')))

        
if __name__ == '__main__':
    unittest.main()
