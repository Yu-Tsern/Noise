import hashlib
from functions import *


class responder(object):
    def __init__(self):
        self.potocal_name = b"Noise_xx()"
        # ephemeral key pair
        self.key = GENERATE_KEYPAIR()
        self.e_pub = self.key.public_key()
        self.e_pri = self.key
        self.re_pub = ""
        self.re_priv = ""
        # s_key: static key pair
        self.s_key = GENERATE_KEYPAIR()
        self.s_pub = self.s_key.public_key()
        self.s_pri = self.s_key
        self.rs = ""
        self.h = ""
        self.ck = 0
        self.k = ""
        self.n = 0
        self.ck1 = ""
        self.ck2 = ""

    def first_stage(self):
        self.h = HASH(self.potocal_name)

        self.ck = self.h

        self.re_pub = GENERATE_KEYPAIR().public_key()
        #self.re_pub = b"This is fake sender's public key"

        self.h = HASH(self.h + self.re_pub.public_bytes())


        self.h = HASH(self.h + self.h)

    # <------------ e, dhee,s,dhse

    def second_stage(self):
        # "e"


        # dhee
        self.h = HASH(self.h + self.e_pub.public_bytes())
        temp = DH(self.e_pri, self.re_pub)
        # self.ck = "new ck from dhee with KDF"
        # self.k = "new key from dhee with FDK"
        self.ck, self.k = HKDF(self.ck, temp, 2)
        self.n = 0

        # s
        self.s_pub = self.s_key.public_key()

        cipher_to_sent = self.h + self.s_pub.public_bytes()
        cipher_to_sent = self.encrypt(self.k, cipher_to_sent)
        self.h = HASH(self.h + cipher_to_sent)

        # dhse
        # For "se": Calls MixKey(DH(s, re)) if initiator, MixKey(DH(e, rs)) otherwise.
        # self.ck = b"new ck from dhse with KDF"
        # self.k = b"new key from dhse with KDF"
        temp = DH(self.s_pri, self.re_pub)
        self.ck, self.k = HKDF(self.ck, temp, 2)
        self.n = 0

        # send payload encrypt with key? empty
        cipher_to_sent = self.h + b"sth"
        cipher_to_sent = self.encrypt(self.k, cipher_to_sent)

        self.h = HASH(self.h + cipher_to_sent)

    def third_stage(self):
        # s
        self.rs = GENERATE_KEYPAIR().public_key()
        #self.rs = b"this is the fake sender's static key from sender"

        cipher_from_sender = b"123"
        self.h = HASH(self.h + cipher_from_sender)

        # dhse
        # For "se": Calls MixKey(DH(s, re)) if initiator, MixKey(DH(e, rs)) otherwise.
        # self.ck = b"new ck from dhse with KDF"
        # self.k = b"new key from dhse with KDF"
        temp = DH(self.e_pri, self.rs)

        # use KDF to get 2 key
        self.ck1, self.ck2 = HKDF(self.ck, temp, 2)


    def encrypt(self, key, plain_text):
        return b"2"
