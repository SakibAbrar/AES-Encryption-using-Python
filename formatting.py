####################################################
#####################SENITIZE#######################

TEXT_SIZE = 16
KEY_SIZE = 16


# plaintext = "Thats my Kung Fu"

def sanitize(str, size = TEXT_SIZE):
    """This function sanitizes any given string passed as parameter `str` 
        and returns a 1D array of 16 characters."""
    return str[:TEXT_SIZE].ljust(TEXT_SIZE, ' ')

def toHexArray(str):
    """This function converts given text block passed as parameter `str` 
        and returns a 1D array of 16 hex string characters."""
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

def readFileToHex(file):
    with open(file, 'rb') as f:
        hexdata = f.read().hex()
    ans = list( map(''.join, zip(*[iter(hexdata)]*2)) )
    # import binascii
    # bytes = binascii.a2b_hex(''.join(ans))
    # bitout = open('dp_cpy.jpg', 'wb')
    # bitout.write(bytes)
    # print(len(ans))
    return ans
# print(readFileToHex('dp.jpg'))


def writeHexToFile(arr, file):
    import binascii
    bytes = binascii.a2b_hex(''.join(arr))
    bitout = open(file, 'wb')
    bitout.write(bytes)
# print(writeHexToFile(readFileToHex('dp.jpg')))
    

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
    return ans
# print(toRowMajor(toHexArray(plaintext)))

def toColumnMajor(arr):
    """This function takes a 1D array passed as `arr` 
    and converts and returns a 2D column major matrix"""
    return transpose(toRowMajor(arr))
# print(toColumnMajor(toHexArray(plaintext)))


def toChunks(hexArray):
    ans = []    
    zeroNeeded = (TEXT_SIZE - len(hexArray) % TEXT_SIZE ) % TEXT_SIZE

    for idx in range(zeroNeeded):
        hexArray.append('00')

    for idx in range( int(len(hexArray) / TEXT_SIZE)):
        ans.append(toColumnMajor(hexArray[idx * TEXT_SIZE: idx * TEXT_SIZE + TEXT_SIZE]))
    return ans
# print(toChunks(readFileToHex('dp.jpg')))

def parseFileToMatrices(file):
    return toChunks(readFileToHex(file))
# print(parseFileToMatrices('dp.jpg'))

def flattenMatrix(mat):
    return [item for sublist in mat for item in sublist]
# print(flattenMatrix([['54', '68', '61', '74'], ['73', '20', '6d', '79'], ['20', '4b', '75', '6e'], ['67', '20', '46', '75']]))


def writeMatricesToFile(m_arr, file):

    for idx in range(len(m_arr)):
        m_arr[idx] = flattenMatrix(transpose(m_arr[idx]))
    last_m = m_arr[len(m_arr)-1]
    while last_m[-1] == '00':
        last_m.pop(-1)
    flattest = flattenMatrix(m_arr)
    print(len(flattest))
    import binascii
    bitout = open(file, 'wb')
    bytes = binascii.a2b_hex(''.join(flattest))
    bitout.write(bytes)
    bitout.close()

# m_arr = parseFileToMatrices('dp.jpg')
# writeMatricesToFile(m_arr, 'dp_copy.jpg')
####################################################
###################SENITIZE END#####################

# plaintext = "Thats my Kung Fu"

# abcdefghijklmnop