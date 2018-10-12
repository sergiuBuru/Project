import unittest
from keys import *

class Test(unittest.TestCase):

    def setUp(self): pass

    def tearDown(self): pass

    def test_01_private_key(self):
        private_key = generate_private_key()
        self.assertIsInstance(private_key, bytes)
        self.assertEqual(len(private_key), 32)

    def test_02_public_key(self):
        private_key = generate_private_key()
        public_key = generate_public_key(private_key)
        self.assertIsInstance(public_key, bytes)

    def test_03_pk_hash(self):
        private_key = generate_private_key()
        public_key = generate_public_key(private_key)
        pk_hash = generate_pk_hash(public_key)
        self.assertIsInstance(pk_hash, bytes)

if __name__ == '__main__':
    unittest.main()

    
