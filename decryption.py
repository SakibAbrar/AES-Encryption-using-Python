from operator import matmul
import formatting
import roundkey
##DECRYPTION CODE WILL GO IN HERE

from BitVector import *

AES_modulus = BitVector(bitstring='100011011')

InvMixer = [
    ["0E", "0B", "0D", "09"],
    ["09", "0E", "0B", "0D"],
    ["0D", "09", "0E", "0B"],
    ["0B", "0D", "09", "0E"]
]

def matrix_xor(mat1, mat2):
    matans = []
    for idx in range(len(mat1)):
        matans.append(roundkey.word_xor(mat1[idx], mat2[idx]))
    return matans

def invShiftRow(mat):
    matans = []
    for idx in range(len(mat)):
        for s in range(idx):
            roundkey.shiftRight(mat[idx])
        matans.append(mat[idx])
    return matans
# print(invShiftRow(state_matrix))

def inv_substitute_matrix(mat):
    matans = []
    for m in mat:
        matans.append(roundkey.inv_substitute_word(m))
    return matans
# print(inv_substitute_matrix(state_matrix))

def rowColumnMul(word1, word2):
    bsum = BitVector(intVal=0, size=8)
    for idx in range(len(word1)):
        b1 = BitVector(intVal=int(word1[idx], 16), size=8)
        b2 = BitVector(intVal=int(word2[idx], 16), size=8)
        bmul = b1.gf_multiply_modular(b2, AES_modulus, 8)
        bsum = bsum.__xor__(bmul)
    return bsum.get_bitvector_in_hex()

def invMixColumn(mat):
    trans_mat = formatting.transpose(mat)
    matans = []
    
    for row in InvMixer:
        matansrow = []
        for col in trans_mat:
            matansrow.append(rowColumnMul(row, col))
        matans.append(matansrow)
    return matans

key = "Thats my Kung Fu"
# text=")ÃP_W ö@"³×:"
state_matrix = [['29', '57', '40', '1a'], ['c3', '14', '22', '02'], ['50', '20', '99', 'd7'], ['5f', 'f6', 'b3', '3a']]
w = roundkey.gen_roundkey(formatting.toRowMajor(formatting.toHexArray(key)))

def round0(mat):
    # #round 0 step 1 add roundkey
    return matrix_xor(state_matrix, formatting.transpose(w.copy()[40:44]))

def regularround(mat, idx):
    # #round 1 step 1 iverse shift row
    mat = invShiftRow(mat)
    # #round 1 step 2 iverse substitiute matrix
    mat = inv_substitute_matrix(mat)
    # #round 1 step 3 add round key
    mat = matrix_xor(mat, formatting.transpose(w.copy()[40 - idx * 4:44 - idx * 4]))
    # #round 1 step 4 add inverse mix column
    mat = invMixColumn(mat)
    return mat

def roundlast(mat):
    mat = invShiftRow(mat)
    mat = inv_substitute_matrix(mat)
    mat = matrix_xor(mat, formatting.transpose(w.copy()[0:4]))
    return mat

def aes128Decrypt(mat, total_round=11):
    mat = round0(mat)
    
    for idx in range(1, total_round-1):
        mat = regularround(mat, idx)

    mat = roundlast(mat)

    return mat

print(aes128Decrypt(state_matrix))
