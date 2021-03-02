####################################################
#####################SENITIZE#######################

TEXT_SIZE = 16
KEY_SIZE = 16


# plaintext = "Thats my Kung Fu"

def sanitize(str, size):
    return str[:TEXT_SIZE].ljust(TEXT_SIZE, ' ')

def toHexArray(str):
    str = sanitize(str, 16)
    return [x.encode('utf-8').hex() for x in str]
# print(toHexArray(plaintext))

def toIntArray(str):
    return [x for x in str]

def transpose(mat):
    temp = mat.copy()
    return [ list(e) for e in zip(*temp)]

def toRowMajor(arr):
    column_size = 4
    ans = []
    for idx in range(column_size, len(arr) + 1, column_size):
        ans.append(arr[idx-column_size:idx])
    return ans
# print(toRowMajor(toHexArray(plaintext)))

def toColumnMajor(arr):
    return transpose(toRowMajor(arr))
# print(toColumnMajor(toHexArray(plaintext)))

####################################################
###################SENITIZE END#####################

# plaintext = "Thats my Kung Fu"

# abcdefghijklmnop