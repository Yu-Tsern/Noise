# These are the functions used in the protocol.
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import hashes, hmac

# DH functions

def GENERATE_KEYPAIR():
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()
    return KeyPair25519(private_key, public_key, public_key.public_bytes())

def DH(key_pair, public_key):
    if not isinstance(private_key, x25519.X25519PrivateKey) or not isinstance(public_key, x25519.X25519PublicKey):
        raise NoiseValueError('Invalid keys! Must be x25519.X25519PrivateKey and x25519.X25519PublicKey instances')
    return private_key.exchange(public_key)


# Cipher function

def ENCRYPT(k, n, ad, plaintext):
    return AESGCM.encrypt(nonce=NONCE(n), data=plaintext, associated_data=ad)

def DECRYPT(k, n, ad, ciphertext):
    return AESGCM.decrypt(nonce=NONCE(n), data=ciphertext, associated_data=ad)

def NONCE(n):
    return b'\x00\x00\x00\x00' + n.to_bytes(length=8, byteorder='big')

def REKEY(k):
    return ENCRYPT(k, MAX_NONCE, b'', b'\x00' * 32)[:32]


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
    print("Hash: ", HASH(b'hello'))
    print("Mac: ", HMAC_HASH(b'key', b'hello'))