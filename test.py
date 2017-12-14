from responder import *
from sender import *

if __name__ == '__main__':
    s = sender()
    r = responder()

    print("first stage: ---->e")
    s.first_stage()
    r.first_stage()

    print("second stage: <---e,dhee,s,dhse")
    s.second_stage()
    r.second_stage()

    print("third stage: ----->s,dhse")
    s.third_stage()
    key1, key2 = r.third_stage()
    print("two keys from handshake:")
    print(b"key1: " + key1)
    print(b"key2:" + key2)
