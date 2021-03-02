####################################################
#####################SENITIZE#######################

TEXT_SIZE = 16
KEY_SIZE = 16

def sanitize(str, size):
    return str[:TEXT_SIZE].ljust(TEXT_SIZE, ' ')

def toHexArray(str):
    str = sanitize(str, 16)
    return [x.encode('utf-8').hex() for x in str]

def toIntArray(str):
    return [x for x in str]

def transpose(mat):
    result = []
    for i in range(len(mat)):
        # iterate through columns
        for j in range(len(mat[0])):
            result[j][i] = mat[i][j]
    
    return result

def toRowMajor(arr):
    column_size = 4
    ans = []
    for idx in range(column_size, len(arr) + 1, column_size):
        ans.append(arr[idx-column_size:idx])
    return ans

def toColumnMajor(arr):
    return transpose(toRowMajor(arr))

####################################################
###################SENITIZE END#####################

# plaintext = "Thats my Kung Fu"
# plaintext = "Thats my Kung Fu"

# abcdefghijklmnop
# print(toRowMajor(toHexArray(plaintext)))