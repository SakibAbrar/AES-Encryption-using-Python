import formatting
import roundkey
##ENCRYPTION CODE WILL GO IN HERE

from BitVector import *

AES_modulus = BitVector(bitstring='100011011')

Mixer = [
    ["02", "03", "01", "01"],
    ["01", "02", "03", "01"],
    ["01", "01", "02", "03"],
    ["03", "01", "01", "02"]
]


def matrix_xor(mat1, mat2):
    matans = []
    for idx in range(len(mat1)):
        matans.append(roundkey.word_xor(mat1[idx], mat2[idx]))
    return matans

def substitute_matrix(mat):
    matans = []
    for m in mat:
        matans.append(roundkey.substitute_word(m))
    return matans

def shiftRow(mat):
    matans = []
    for idx in range(len(mat)):
        for s in range(idx):
            roundkey.shiftLeft(mat[idx])
        matans.append(mat[idx])
    return matans

def rowColumnMul(word1, word2):
    bsum = BitVector(intVal=0, size=8)
    for idx in range(len(word1)):
        b1 = BitVector(intVal=int(word1[idx], 16), size=8)
        b2 = BitVector(intVal=int(word2[idx], 16), size=8)
        bmul = b1.gf_multiply_modular(b2, AES_modulus, 8)
        bsum = bsum.__xor__(bmul)
    return bsum.get_bitvector_in_hex()
# print(rowColumnMul(["02", "03", "01", "01"], ['63', '2f', 'af', 'a2']))


def mixColumn(mat):
    trans_mat = formatting.transpose(mat)
    matans = []
    
    for row in Mixer:
        matansrow = []
        for col in trans_mat:
            matansrow.append(rowColumnMul(row, col))
        matans.append(matansrow)
    return matans


def shiftColumn(mat):
    pass 


key="Thats my Kung Fu"
text="Two One Nine Two"
state_matrix = formatting.toColumnMajor(formatting.toHexArray(text))
# print("state_matrix", state_matrix)
w = roundkey.gen_roundkey(formatting.toRowMajor(formatting.toHexArray(key)))
# print("w", w[0:4])

def round0(mat):
    return matrix_xor(state_matrix, formatting.transpose(w.copy()[0:4]))

def regularround(mat, idx):
    mat = substitute_matrix(mat)
    mat = shiftRow(mat)
    mat = mixColumn(mat)
    mat = matrix_xor(mat, formatting.transpose(w.copy()[4*idx:4*idx+4]))
    return mat

def roundlast(mat):
    mat = substitute_matrix(mat)
    mat = shiftRow(mat)
    return matrix_xor(mat ,formatting.transpose(w.copy()[40:44]))

# #round 0 step 1 add roundkey
# state_matrix = matrix_xor(state_matrix, formatting.transpose(w.copy()[0:4]))
# # print(state_matrix)

# #round 1 step 1 substitute bytes
# state_matrix = substitute_matrix(state_matrix)
# # print(state_matrix)

# #round 1 step 2 shift row
# state_matrix = shiftRow(state_matrix)
# # print(state_matrix)

# #round 1 step 3 mix column
# state_matrix = mixColumn(state_matrix)
# # print(state_matrix)

# #round 1 step 4 add roundkey
# state_matrix = matrix_xor(state_matrix, formatting.transpose(w.copy()[4:8]))

def aes128Encrypt(mat, total_round=11):
    mat = round0(mat)
    
    for idx in range(1, total_round-1):
        mat = regularround(mat, idx)

    mat = roundlast(mat)

    return mat

#main run
# aes128Encrypt(state_matrix)
state_matrix = aes128Encrypt(state_matrix)

def hexArrayToText(mat):
    print(mat)
    trans_mat = formatting.transpose(mat)
    print(trans_mat)
    cypher_text = ""
    for row in trans_mat:
        for ele in row:
            cypher_text = cypher_text + chr(int(ele, 16))
    print(cypher_text)

hexArrayToText(state_matrix)
