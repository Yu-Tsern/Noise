# These are the functions used in the protocol.
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import hashes, hmac

# DH functions

def GENERATE_KEYPAIR():
    return x25519.X25519PrivateKey.generate()

def DH(private_key, public_key):
    return private_key.exchange(public_key)


# Cipher functions use aesgcm


# Hash functions
hashlen = 32
blocklen = 64

def HASH(data):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(data)
    return digest.finalize()

def HMAC_HASH(key, data):
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(data)
    return h.finalize()

def HKDF(chaining_key, input_key_material, num_outputs):
    temp_key = HMAC_HASH(chaining_key, input_key_material)
    output1 = HMAC_HASH(temp_key, b'\x01')
    output2 = HMAC_HASH(temp_key, output1 + b'\x02')
    if num_outputs == 2:
        return output1, output2
    output3 = HMAC_HASH(temp_key, output2 + b'\x03')
    return output1, output2, output3



if __name__ == "__main__":
    key1 = GENERATE_KEYPAIR()
    key2 = GENERATE_KEYPAIR()
    print("DH(key1, key2_public): ", DH(key1, key2.public_key()))
    print("DH(key1, key2_public): ", DH(key1, key2.public_key()))

    nonce = os.urandom(12)
    aad = b"authenticated but unencrypted data"
    key = AESGCM.generate_key(bit_length=128)
    aesgcm1 = AESGCM(key)
    aesgcm2 = AESGCM(key)
    pt = b"a secret message"
    ct = aesgcm1.encrypt(nonce, pt, aad)
    rt = aesgcm2.decrypt(nonce, ct, aad)
    print("Plaintext: ", pt)
    print("Ciphertext: ", ct)
    print("Recovertext: ", rt)


    print("Mac: ", HMAC_HASH(b'key', b'hello'))
