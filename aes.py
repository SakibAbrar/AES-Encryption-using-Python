

from BitVector import *
import sys, getopt
import time


#192 bit
# TEXT_SIZE = 16
# ROW_SIZE = 4
# ROUND = 10
#192 bit
# TEXT_SIZE = 24
# ROW_SIZE = 6
# ROUND = 12
#256 bit
TEXT_SIZE = 32
ROW_SIZE = 8
ROUND = 14

####################################################
#####################SENITIZE#######################

# plaintext = "Thats my Kung Fu"

def sanitize(str, size = TEXT_SIZE):
    """This function sanitizes any given string passed as parameter `str` 
        and returns a 1D array of `TEXT_SIZE` characters."""
    return str[:TEXT_SIZE].ljust(TEXT_SIZE, ' ')

def toHexArray(str):
    """This function converts given text block passed as parameter `str` 
        and returns a 1D array of `TEXT_SIZE` hex string characters."""
    str = sanitize(str)
    return [x.encode('utf-8').hex() for x in str]
# print(toHexArray(plaintext))

def toSanitizedChunks(text):
    """This function takes a text passed as parameter `text` 
        and returns sanitized chunks of `TEXT_SIZE` size"""
    ans = []
    for idx in range(0, len(text), TEXT_SIZE):
        ans.append(sanitize(text[idx: idx + TEXT_SIZE]))
    return ans
# print(toSanitizedChunks("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."))
    

def transpose(mat):
    """This function takes a 2D matrix passed as `mat` and then transposes and returns the new matrix"""
    temp = mat.copy()
    return [ list(e) for e in zip(*temp)]


def toRowMajor(arr):
    """This function takes a 1D array passed as `arr` 
    and converts and returns a 2D row major matrix"""

    column_size = 4
    ans = []
    for idx in range(column_size, len(arr) + 1, column_size):
        ans.append(arr[idx-column_size:idx])
    # print(ans)
    return ans
# print(toRowMajor(toHexArray(plaintext)))

def toColumnMajor(arr):
    """This function takes a 1D array passed as `arr` 
    and converts and returns a 2D column major matrix"""
    # print(transpose(toRowMajor(arr)))
    return transpose(toRowMajor(arr))
# print(toColumnMajor(toHexArray(plaintext)))


def readFileToHex(file):
    with open(file, 'rb') as f:
        hexdata = f.read().hex()
    ans = list( map(''.join, zip(*[iter(hexdata)]*2)) )
    return ans
# print(readFileToHex('dp.jpg'))

def toChunks(hexArray):
    ans = []    
    zeroNeeded = (TEXT_SIZE - len(hexArray) % TEXT_SIZE ) % TEXT_SIZE

    for idx in range(zeroNeeded):
        hexArray.append('00')

    for idx in range( int(len(hexArray) / TEXT_SIZE)):
        ans.append(toColumnMajor(hexArray[idx * TEXT_SIZE: idx * TEXT_SIZE + TEXT_SIZE]))
    # print(ans)
    return ans
# print(toChunks(readFileToHex('smallest.pdf'))[0])
# print(toChunks(toHexArray('abcd')))

def parseFileToMatrices(file):
    return toChunks(readFileToHex(file))
# print(parseFileToMatrices('dp.jpg'))

def flattenMatrix(mat):
    return [item for sublist in mat for item in sublist]
# print(flattenMatrix([['54', '68', '61', '74'], ['73', '20', '6d', '79'], ['20', '4b', '75', '6e'], ['67', '20', '46', '75']]))

def twoDHexToText(mat):
    trans_mat = transpose(mat)
    cypher_text = ""
    for row in trans_mat:
        for ele in row:
            cypher_text = cypher_text + chr(int(ele, 16))
    return cypher_text
# print(twoDHexToText(toChunks(readFileToHex('smallest.pdf'))[0]))

def writeMatricesToFile(m_arr, file):

    for idx in range(len(m_arr)):
        m_arr[idx] = flattenMatrix(transpose(m_arr[idx]))
    last_m = m_arr[len(m_arr)-1]
    while last_m[-1] == '00':
        last_m.pop(-1)
    flattest = flattenMatrix(m_arr)
    import binascii
    bitout = open(file, 'wb')
    bytes = binascii.a2b_hex(''.join(flattest))
    bitout.write(bytes)
    bitout.close()
# m_arr = parseFileToMatrices('dp.jpg')
# writeMatricesToFile(m_arr, 'dp_copy.jpg')

####################################################
###################SENITIZE END#####################


####################################################
###################GENERATE KEY#####################

REP = 0

AES_modulus = BitVector(bitstring='100011011')

Sbox = [None] * 256
InvSbox = [None] * 256

def genSboxInvSbox():
    for i in range(256):
        if i == 0:
            Sbox[i] = '63'
            InvSbox[0x63] = hex(i)[2:].rjust(2, ' ')
            continue
        b = BitVector(intVal=i, size=8).gf_MI(AES_modulus, 8)
        ans_int = b.int_val() ^ (b << 1).int_val() ^ (b << 1).int_val() ^ (b << 1).int_val() ^ (b << 1).int_val() ^ int('63', 16)
        Sbox[i] = hex(ans_int)[2:].rjust(2, ' ')
        InvSbox[ans_int] = hex(i)[2:].rjust(2, ' ')
genSboxInvSbox()
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
        b = Sbox[int(w, 16)]
        new_word.append(b)
    return new_word
# print(substitute_word(['20', '46', '75', '67']))

def inv_substitute_word(word):
    new_word = []
    for w in word:
        b = InvSbox[int(w, 16)]
        new_word.append(b)
    return new_word


def gen_round_const():
    first = '01'
    b2 = BitVector(intVal=2, size=8)
    b11 = BitVector(hexstring="11")
    b = BitVector(intVal=int(first, 16), size=8)

    global REP
    for idx in range(REP):
        b = b.gf_multiply_modular(b2, AES_modulus, 8)
        if idx >= 128:
            b = b.__xor__(b11)
    REP = REP + 1
    return [b.get_bitvector_in_hex(), '00', '00', '00']


def add_round_const(word):
    result = []
    add_word = gen_round_const()
    for idx in range(len(word)):
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
    for idx in range(len(word1)):
        b1 = BitVector(intVal=int(word1[idx], 16), size=8)
        b2 = BitVector(intVal=int(word2[idx], 16), size=8)
        result.append(b1.__xor__(b2).get_bitvector_in_hex())
    # print("xor", result)
    return result
# print(word_xor(['E2', '32', 'FC', 'F1'], ['73', '20', '6D', '79']))


def gen_one_round(w):
    w_len = len(w)
    w.append(word_xor(w[w_len - ROW_SIZE], g(w[w_len - 1 ]))) # w[0],g(w[3])
    for idx in range(ROW_SIZE-1, 0, -1):
        w.append(word_xor(w[w_len - idx], w[w_len + (ROW_SIZE - idx - 1)])) # w[1],w[4]
    
    
def gen_roundkey(w, rounds=ROUND):
    for r in range(rounds):
        gen_one_round(w)
    return w

# key = [['54', '68', '61', '74'], ['73', '20', '6d', '79'], ['20', '4b', '75', '6e'], ['67', '20', '46', '75']]
# print(gen_roundkey(key))

####################################################
#################GENERATE KEY END###################


####################################################
#################ENCRYPTION START###################


Mixer = [
    ["02", "03", "01", "01"],
    ["01", "02", "03", "01"],
    ["01", "01", "02", "03"],
    ["03", "01", "01", "02"]
]

def matrix_xor(mat1, mat2):
    matans = []
    for idx in range(len(mat1)):
        matans.append(word_xor(mat1[idx], mat2[idx]))
    # print(matans)
    return matans

def substitute_matrix(mat):
    matans = []
    for m in mat:
        matans.append(substitute_word(m))
    return matans

def shiftRow(mat):
    matans = []
    for idx in range(len(mat)):
        for s in range(idx):
            shiftLeft(mat[idx])
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
    trans_mat = transpose(mat)
    matans = []
    # print(trans_mat)
    for row in Mixer:
        matansrow = []
        for col in trans_mat:
            matansrow.append(rowColumnMul(row, col))
        matans.append(matansrow)
    # print(matans)
    return matans


key="Thats my Kung Fu. Is it?"
# state_matrix = toColumnMajor(toHexArray(text))
# print("state_matrix", state_matrix)
w = ['00' * ROW_SIZE] * ((ROUND+1)*ROW_SIZE)
print(len(w))
# print("w", w[0:4])


def aes128Encrypt(mat, total_round=ROUND + 1):

    def round0(mat):
        return matrix_xor(mat, transpose(w.copy()[0:ROW_SIZE]))

    def regularround(mat, idx):
        mat = substitute_matrix(mat)
        mat = shiftRow(mat)
        mat = mixColumn(mat)
        mat = matrix_xor(mat, transpose(w.copy()[ROW_SIZE*idx : ROW_SIZE*idx+ROW_SIZE]))
        return mat

    def roundlast(mat):
        mat = substitute_matrix(mat)
        mat = shiftRow(mat)
        return matrix_xor(mat ,transpose(w.copy()[ROW_SIZE * ROUND: ROW_SIZE * (ROUND + 1)]))


    mat = round0(mat)
    
    for idx in range(1, total_round-1):
        mat = regularround(mat, idx)

    mat = roundlast(mat)

    return mat

#main run
# aes128Encrypt(state_matrix)
# state_matrix = aes128Encrypt(state_matrix)

def hexArrayToText(mat):
    print(mat)
    trans_mat = transpose(mat)
    print(trans_mat)
    cypher_text = ""
    for row in trans_mat:
        for ele in row:
            cypher_text = cypher_text + chr(int(ele, 16))
    print(cypher_text)
# hexArrayToText(state_matrix)

def encryptText(text):
    return aes128Encrypt(toColumnMajor(toHexArray(text)))

def encryptFile(file):
    m_arr = parseFileToMatrices(file)
    print("Matrices:",len(m_arr))
    len_m_arr = len(m_arr)
    for idx in range(len(m_arr)):
        print(idx, "/", len_m_arr, " done")
        m_arr[idx] = aes128Encrypt(m_arr[idx])
    writeMatricesToFile(m_arr, file)


####################################################
#################ENCRYPTION END###################


####################################################
#################DECRYPTION START###################

InvMixer = [
    ["0E", "0B", "0D", "09"],
    ["09", "0E", "0B", "0D"],
    ["0D", "09", "0E", "0B"],
    ["0B", "0D", "09", "0E"]
]


def invShiftRow(mat):
    matans = []
    for idx in range(len(mat)):
        for s in range(idx):
            shiftRight(mat[idx])
        matans.append(mat[idx])
    return matans
# print(invShiftRow(state_matrix))

def inv_substitute_matrix(mat):
    matans = []
    for m in mat:
        matans.append(inv_substitute_word(m))
    return matans
# print(inv_substitute_matrix(state_matrix))

def invMixColumn(mat):
    trans_mat = transpose(mat)
    matans = []
    
    for row in InvMixer:
        matansrow = []
        for col in trans_mat:
            matansrow.append(rowColumnMul(row, col))
        matans.append(matansrow)
    return matans


def aes128Decrypt(mat, total_round=ROUND + 1):

    def round0(mat):
        # #round 0 step 1 add roundkey
        return matrix_xor(mat, transpose(w.copy()[ROW_SIZE*ROUND:ROW_SIZE*(ROUND + 1)]))

    def regularround(mat, idx):
        # #round 1 step 1 iverse shift row
        mat = invShiftRow(mat)
        # #round 1 step 2 iverse substitiute matrix
        mat = inv_substitute_matrix(mat)
        # #round 1 step 3 add round key
        mat = matrix_xor(mat, transpose(w.copy()[ROW_SIZE*ROUND - idx * ROW_SIZE:ROW_SIZE*(ROUND + 1) - idx * ROW_SIZE]))
        # #round 1 step 4 add inverse mix column
        mat = invMixColumn(mat)
        return mat

    def roundlast(mat):
        mat = invShiftRow(mat)
        mat = inv_substitute_matrix(mat)
        mat = matrix_xor(mat, transpose(w.copy()[0:ROW_SIZE]))
        return mat

    mat = round0(mat)
    
    for idx in range(1, total_round-1):
        mat = regularround(mat, idx)

    mat = roundlast(mat)

    return mat
# print(aes128Decrypt(state_matrix))

def decryptText(text):
    return aes128Decrypt(toColumnMajor(toHexArray(text)))

def decryptFile(file):
    m_arr = parseFileToMatrices(file)
    print("Matrices:",len(m_arr))
    len_m_arr = len(m_arr)
    for idx in range(len(m_arr)):
        print(idx, "/", len_m_arr, " done")
        m_arr[idx] = aes128Decrypt(m_arr[idx])
    writeMatricesToFile(m_arr, file)


####################################################
#################DECRYPTION END###################


####################################################
#################TEST START###################


# encryptFile('smallest.pdf')
# decryptFile('smallest.pdf')


def main(argv):
    # starting time
    starttime = time.time()
    try:
        opts, args = getopt.getopt(argv,"k:edbf:s:",["encrypt=","decrypt="])
    except getopt.GetoptError:
        print('python aes128.py -k <key> -e -d -b -s <string> -f <file>')
        sys.exit(2)
    mode = 128
    w = gen_roundkey(toRowMajor(toHexArray(key)))
    type = 1
    for opt, value in opts:
        if opt in ("-k", "--key"):
            w = gen_roundkey(toRowMajor(toHexArray(value)))
        elif opt in ("-e", "--encrypt"):
            type = 1
        elif opt in ("-d", "--decrypt"):
            type = 2
        elif opt in ("-b", "--both"):
            type = 3
        elif opt in ("-f", "--file"):
            if type == 1:
                print("Encrypting...")
                encryptFile(value)
                print("Encrypting Finished!")
            elif type == 2:
                print("Decrypting...")
                decryptFile(value)
                print("Decrypting Finished!")
            elif type == 3:
                print("Encrypting...")
                encryptFile(value)
                print("Encrypting Finished!")
                print("Decrypting...")
                decryptFile(value)
                print("Decrypting Finished!")
        elif opt in ("-s", "--string"):
            if type == 1:
                print("Encrypted:", twoDHexToText(encryptText(value)))
            elif type == 2:
                print("Decrypted:", twoDHexToText(decryptText(value)))
            elif type == 3:
                mat = encryptText(value)
                # print(mat)
                print("Encrypted:", twoDHexToText(mat))
                # print(mat)
                mat = aes128Decrypt(mat)
                print("Decrypted:", twoDHexToText(mat))
    endtime = time.time()
    print("Time Taken:", (endtime - starttime), "sec")

       

if __name__ == "__main__":
    main(sys.argv[1:])


####################################################
#################TEST END###################