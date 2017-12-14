import hashlib
from functions import *

sender_e_keypair = GENERATE_KEYPAIR()
sender_s_keypair = GENERATE_KEYPAIR()


class sender(object):
    def __init__(self):
        self.potocal_name = b"Noise_xx()"
        # ephemeral key pair
        self.key = sender_e_keypair
        self.e_pub = self.key.public_key()
        self.e_pri = self.key
        self.re_pub = ""
        self.re_priv = ""
        # s_key: static key pair
        self.s_key = sender_s_keypair
        self.s_pub = self.s_key.public_key()
        self.s_pri = self.s_key
        self.rs = ""
        self.h = ""
        self.ck = 0
        self.k = ""
        self.n = 0
        self.ck1 = ""
        self.ck2 = ""

    # ------------> e


    def first_stage(self):
        self.h = HASH(self.potocal_name)
        self.ck = self.h

        # sent to other side  e_pub-------->
        # the payload can be certificate, or empty

        self.h = HASH(self.h + self.e_pub.public_bytes())
        self.h = HASH(self.h + self.h)

    # <------------ e, dhee,s,dhse

    def second_stage(self, responder_e_pub, responder_s_pub):
        "e"
        self.re_pub = responder_e_pub
        print("sender get responder's ephemeral public key")
        # self.re_pub = b"This is fake responder's public key"
        self.h = HASH(self.h + self.re_pub.public_bytes())

        # dhee?
        print("sender preformed hdee and get new chaining key:ck, from KDF function")
        temp = DH(self.e_pri, self.re_pub)
        self.ck, self.k = HKDF(self.ck, temp, 2)
        # self.ck = b"new ck from dhee with KDF"
        # self.k = b"new key from dhee with FDK"
        self.n = 0

        # "S"
        print("sender get responder's static key")
        self.rs = responder_s_pub
        # self.rs = b"This is the fake responder's static key from responder"
        cipher_from_responder = b"123"
        self.h = HASH(self.h + cipher_from_responder)

        # dhse
        print("sender preformed hdse and get new chaining key:ck, from KDF function")
        # For "se": Calls MixKey(DH(s, re)) if initiator, MixKey(DH(e, rs)) otherwise.
        # self.ck = b"new ck from dhse with KDF"
        # self.k = b"new key from dhse with KDF"
        temp = DH(self.e_pri, self.rs)
        self.ck, self.k = HKDF(self.ck, temp, 2)
        self.n = 0

    # --------------> s, dhse

    def third_stage(self):
        # s
        self.s_pub = self.s_key.public_key()
        # sent it to responder
        cipher_to_sent = self.h + self.s_pub.public_bytes()
        cipher_to_sent = self.encrypt(self.k, cipher_to_sent)
        self.h = HASH(self.h + cipher_to_sent)

        # dhse
        print("sender preformed hdse and get new chaining key:ck, from KDF function")
        # For "se": Calls MixKey(DH(s, re)) if initiator, MixKey(DH(e, rs)) otherwise.
        # self.ck = b"new ck from dhse with KDF"
        # self.k = b"new key from dhse with KDF"
        temp = DH(self.s_pri, self.re_pub)

        self.ck1, self.ck2 = HKDF(self.ck, temp, 2)
        return self.ck1, self.ck2
        self.n = 0

    def encrypt(self, key, plain_text):
        return b"123"
