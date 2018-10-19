import unittest
from transaction import *
from keys import *

class Test(unittest.TestCase):

    def setUp(self):
        self.k = generate_key_set()

    def tearDown(self): pass

    def test_01_mint(self):
        value = 50000000
        coinbase = mint(self.k['pk_hash'], value)
        self.assertEqual(coinbase['output']['value'], value)
        self.assertEqual(coinbase['output']['locking_script'], to_string(self.k['pk_hash']))
        self.assertEqual(coinbase['hash'], hash_SHA(to_string(self.k['pk_hash']) + str(value)))

    def test_02_create_tx(self):
        value = 5000000000
        coinbase = mint(self.k['pk_hash'], value)
        tx = create_transaction(coinbase, self.k['private'], value)
        prev_tx_hash = tx['input']['previous_tx_hash']
        self.assertEqual(prev_tx_hash, coinbase['hash'])
        vk_string = tx['input']['unlocking_script']['public_key']
        vk = ecdsa.VerifyingKey.from_string(vk_string, ecdsa.SECP256k1)
        sig = tx['input']['unlocking_script']['signature']
        sig = unhexlify(sig)
        unsigned_tx_hash = tx['input']['unlocking_script']['unsigned_tx_hash'].encode()
        self.assertTrue(vk.verify(sig, unsigned_tx_hash))
        self.assertEqual(tx['output']['locking_script'], hexlify(self.k['pk_hash']).decode())
        self.assertEqual(tx['output']['value'], value)

if __name__ == '__main__':
    unittest.main()

    
