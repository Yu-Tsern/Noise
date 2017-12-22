from responder import *
from sender import *

# reference:  https://www.youtube.com/watch?v=ceGTgqypwnQ
# reference: http://noiseprotocol.org/noise.html

if __name__ == '__main__':
    s = sender()
    r = responder()

    print("first stage: ---->e")

    s.first_stage()
    r.first_stage(sender_e_keypair.public_key())
    print("")
    print("second stage: <---e,dhee,s,dhse")

    s.second_stage(responder_e_keypair.public_key(), responder_s_keypair.public_key())
    r.second_stage()
    print("")
    print("third stage: ----->s,dhse")
    print("")

    s_key1, s_key2 = s.third_stage()
    r_key1, r_key2 = r.third_stage(sender_s_keypair.public_key())
    print("")
    print("two keys from handshake for sender:")
    print(b"s.key1: " + s_key1)
    print(b"s.key2: " + s_key2)

    print("")
    print("two keys from handshake for responder:")
    print(b"r.key1: " + r_key1)
    print(b"r.key2: " + r_key2)
    print("")
    print("handshake is done, both party have their symmetric session keys")
