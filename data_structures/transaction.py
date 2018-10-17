from keys import generate_public_key, generate_pk_hash
from binascii import hexlify
from keys import hash_SHA
import ecdsa


def to_string(bytes):
    return hexlify(bytes).decode()

"""
Transactions
"""


def create_transaction(previous_tx, private_key, value, recipient=None):
    public_key = generate_public_key(private_key)
    if not recipient:
        pk_hash = generate_pk_hash(public_key)
    else:
        pk_hash = recipient
    output = {
        'locking_script': hexlify(pk_hash).decode(),
        'value': value
    }
    unsigned_tx = previous_tx['hash'] + \
        previous_tx['output']['locking_script'] + \
        to_string(pk_hash) + str(value)
    unsigned_tx_hash = hash_SHA(unsigned_tx)
    signing_key = ecdsa.SigningKey.from_string(
        private_key, curve=ecdsa.SECP256k1)
    signature = signing_key.sign(unsigned_tx.encode())
    hash_ = hash_SHA(previous_tx['hash'] +
                     to_string(signature) +
                     to_string(pk_hash) +
                     str(value))
    input_ = {
        'previous_tx_hash': previous_tx['hash'],
        'unlocking_script': {
            'unsigned_tx_hash': unsigned_tx_hash,
            'signature': hexlify(signature).decode(),
            'public_key': public_key
        }
    }
    return {
        'input': input_,
        'output': output,
        'hash': hash_
    }

def mint(pk_hash, value):
    string_hash = to_string(pk_hash)
    output = {
        'locking_script': string_hash,
        'value': value
    }
    hash_ = hash_SHA(string_hash + str(value))
    return {
        'output': output,
        'hash': hash_
    }
