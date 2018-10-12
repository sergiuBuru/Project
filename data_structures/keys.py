import os, ecdsa, hashlib, json
from binascii import hexlify, unhexlify

def hash_SHA(string):
    return hexlify(hashlib.sha256(string.encode()).digest()).decode()

def generate_private_key():
    """
    """
    return os.urandom(32)

def generate_public_key(private_key):
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    return verifying_key.to_string()

def generate_pk_hash(public_key):
    hashed_pk = hashlib.sha256(public_key)
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashed_pk.digest())
    return ripemd160.digest()

def generate_key_set():
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    pk_hash = generate_pk_hash(public_key)
    return {
        'private': private_key,
        'public': public_key,
        'pk_hash': pk_hash
    }



