from responder import *
from sender import *

if __name__ == '__main__':
    s = sender()
    r = responder()
    s.first_stage()
    r.first_stage()

    s.second_stage()
    r.second_stage()

    s.third_stage()
    r.third_stage()
