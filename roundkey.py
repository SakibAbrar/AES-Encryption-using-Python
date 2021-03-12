import time

# starting time
# start = time.time()

from operator import xor
from BitVector import *


####################################################
###################GENERATE KEY#####################

REP = 0

AES_modulus = BitVector(bitstring='100011011')

Sbox = [0x00] * 256
InvSbox = [0x00] * 256

for i in range(256):
    if i == 0:
        Sbox[i] = 0x63
        continue
    b = BitVector(intVal=i, size=8).gf_MI(AES_modulus, 8)
    ans_int = b.int_val() ^ (b << 1).int_val() ^ (b << 1).int_val() ^ (b << 1).int_val() ^ (b << 1).int_val() ^ int('63', 16)
    Sbox[i] = ans_int
    InvSbox[ans_int] = i

# print(Sbox[int('63', 16)])

def shiftRight(word):
    word.insert(0, word.pop())
    return word 


def shiftLeft(word):
    word.append(word.pop(0))
    return word
# print(shiftLeft(['67', '20', '46', '75']))

def substitute_word(word):
    new_word = []
    for w in word:
        b = BitVector(intVal=Sbox[int(w, 16)], size=8).get_bitvector_in_hex()
        new_word.append(b)
    return new_word
# print(substitute_word(['20', '46', '75', '67']))

def inv_substitute_word(word):
    new_word = []
    for w in word:
        b = BitVector(intVal=InvSbox[int(w, 16)], size=8).get_bitvector_in_hex()
        new_word.append(b)
    return new_word


def gen_round_const():
    first = '01'
    b2 = BitVector(intVal=2, size=8)
    b = BitVector(intVal=int(first, 16), size=8)

    global REP
    for idx in range(REP):
        b = b.gf_multiply_modular(b2, AES_modulus, 8)
    REP = REP + 1
    return [b.get_bitvector_in_hex(), '00', '00', '00']


def add_round_const(word):
    result = []
    add_word = gen_round_const()
    for idx in range(4):
        b1 = BitVector(intVal=int(word[idx], 16), size=8)
        b2 = BitVector(intVal=int(add_word[idx], 16), size=8)
        result.append(b1.__xor__(b2).get_bitvector_in_hex())
    return result
# print(add_round_const(['B7', '5A', '9D', '85']))

def g(word):
    return add_round_const(substitute_word(shiftLeft(word.copy())))
# print(g(['67', '20' ,'46', '75']))

def word_xor(word1, word2):
    result = []
    for idx in range(4):
        b1 = BitVector(intVal=int(word1[idx], 16), size=8)
        b2 = BitVector(intVal=int(word2[idx], 16), size=8)
        result.append(b1.__xor__(b2).get_bitvector_in_hex())
    return result
# print(word_xor(['E2', '32', 'FC', 'F1'], ['73', '20', '6D', '79']))


def gen_one_round(w):
    idx = len(w)
    w.append(word_xor(w[idx - 4], g(w[idx - 1 ]))) # w[0],g(w[3])
    w.append(word_xor(w[idx - 3], w[idx])) # w[1],w[4]
    w.append(word_xor(w[idx - 2], w[idx + 1])) # w[2],w[5]
    w.append(word_xor(w[idx - 1], w[idx + 2])) # w[3],w[6]
    
def gen_roundkey(w, rounds=10):
    for r in range(rounds):
        gen_one_round(w)
    return w

# key = [['54', '68', '61', '74'], ['73', '20', '6d', '79'], ['20', '4b', '75', '6e'], ['67', '20', '46', '75']]
# print(key[0])
# print(key[3])
# print(gen_roundkey(key))
# gen_one_round(key)

####################################################
#################GENERATE KEY END###################


# text = "Thats my Kung Fu"

# print(gen_roundkey(key))
# end = time.time()
# print("Time taken:", (end-start)/1000, "sec")