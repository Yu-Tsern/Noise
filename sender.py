import hashlib
from functions import *


class sender(object):
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

    # ------------> e


    def first_stage(self):
        self.h = HASH(self.potocal_name)
        self.ck = self.h

        # sent to other side  e_pub-------->
        # the payload can be certificate, or empty
        self.h = HASH(self.h + self.e_pub)
        self.h = HASH(self.h + self.h)

    # <------------ e, dhee,s,dhse

    def second_stage(self):
        "e"
        self.re_pub = b"This is fake responder's public key"
        self.h = HASH(self.h + self.re_pub)

        # dhee?
        temp = DH(self.e_pri, self.re_pub)
        self.ck, self.k = HKDF(self.ck, temp, 2)
        # self.ck = b"new ck from dhee with KDF"
        # self.k = b"new key from dhee with FDK"
        self.n = 0

        # "S"

        self.rs = b"This is the fake responder's static key from responder"
        cipher_from_responder = b"123"
        self.h = HASH(self.h + cipher_from_responder)

        # dhse
        # For "se": Calls MixKey(DH(s, re)) if initiator, MixKey(DH(e, rs)) otherwise.
        # self.ck = b"new ck from dhse with KDF"
        # self.k = b"new key from dhse with KDF"
        temp = DH(self.e_pub, self.rs)
        self.ck, self.k = HKDF(self.ck, temp, 2)
        self.n = 0

    # --------------> s, dhse

    def third_stage(self):
        # s
        self.s_pub = self.s_key.public_key()
        # sent it to responder
        cipher_to_sent = self.h + self.s_pub
        cipher_to_sent = self.encrypt(self.k, cipher_to_sent)
        self.h = HASH(self.h + cipher_to_sent)

        # dhse
        # For "se": Calls MixKey(DH(s, re)) if initiator, MixKey(DH(e, rs)) otherwise.
        # self.ck = b"new ck from dhse with KDF"
        # self.k = b"new key from dhse with KDF"
        temp = DH(self.s_pub, self.re_pub)
        self.ck, self.k = HKDF(self.ck, temp, 2)

        self.n = 0

    def encrypt(self, key, plain_text):
        return b"123"
