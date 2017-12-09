import hashlib


class responder(object):
    def __init__(self):
        self.potocal_name = b"Noise_xx()"
        self.e_pub = ""
        self.e_pri = ""
        self.re_pub = ""
        self.re_priv = ""
        self.s = ""
        self.rs = ""
        self.h = ""
        self.ck = 0
        self.k = ""
        self.n = 0

    def first_stage(self):
        self.h = hashlib.sha256()
        self.h.update(self.potocal_name)
        self.ck = self.h

        self.re_pub = b"This is fake sender's public key"
        self.h.update(self.re_pub)

        self.h.update(self.re_pub)
        self.h.update(self.h)

    # <------------ e, dhee,s,dhse

    def second_stage(self):
        # "e"

        self.e_pub = b"This is fake responder's public key"

        # dhee

        self.h.update(self.e_pub)
        self.ck = "new ck from dhee with KDF"
        self.k = "new key from dhee with FDK"
        self.n = 0

        # s
        self.s = b"This is the fake responder's static key"

        cipher_to_sent = self.h + self.s
        cipher_to_sent = self.encrypt(self.k, cipher_to_sent)
        self.h.update(cipher_to_sent)

        # dhse
        self.ck = b"new ck from dhse with KDF"
        self.k = b"new k from dhse with KDF"
        self.n = 0

        # send payload encrypt with key? empty
        cipher_to_sent = self.h + b"sth"
        cipher_to_sent = self.encrypt(self.k, cipher_to_sent)

        self.h.update(cipher_to_sent)

    def third_stage(self):
        # s
        self.rs = b"this is the fake sender's static key"
        cipher_from_sender = b"123"
        self.h.update(cipher_from_sender)

        # dhse
        self.ck = b"new ck from dhse with KDF"
        self.k = b"new key from dhse with KDF"

        self.ck1 = b"from ck"
        self.ck2 = b"from ck"

    def dhee(self):
        return 1

    def dhse(self):
        return 1

    def KDF(self):
        return 1

    def encrypt(self, key, plain_text):
        return b"2"
