from bitarray import bitarray
import numpy as np
from time import process_time


# getting data from user
path = input("please enter file path: ")
file = open(path, encoding="utf8")
data = file.read()
file.close()

t1_start = process_time()

# initialisation of lists
flag_buffer = bitarray()
alphabet = []
prob = {}

# getting probability of each character
for symbol in data:
    if symbol in prob.keys():
        prob[symbol] += 1
    else:
        prob[symbol] = 1
        alphabet.append(symbol)

pivot = len(alphabet) // 2
index = 0
i = 0

# re-arranging alphabet
while len(prob) != 0:
    character = max(prob, key=prob.get)
    if i % 2:
        index += 1
        alphabet[len(alphabet) - index] = character
        prob.pop(max(prob, key=prob.get))
    else:
        alphabet[index] = character
        prob.pop(max(prob, key=prob.get))
    i += 1

toWrite = ''
dict = {}
# saving alphabet
# optimization: using dictionary instead of array to get the distance
for i in range(len(alphabet)):
    toWrite += alphabet[i]
    if alphabet[i] not in dict.keys():
        dict[alphabet[i]] = pivot - i

a = open('alphabet.txt', 'w', encoding="utf8")
a.write(toWrite)
a.close()

if len(alphabet) >= 512:
    distances = np.zeros(len(data), dtype=np.uint16)
else:
    distances = np.zeros(len(data), dtype=np.uint8)

i = 0

# getting distances
for symbol in data:
    if dict[symbol] >= 0:
        flag_buffer.append(True)
        distances[i] = abs(dict[symbol])
    else:
        flag_buffer.append(False)
        distances[i] = abs(dict[symbol])
    i += 1

flags = np.array(flag_buffer, dtype=np.int8)
flags.tofile('flags.npy')
i = '0'
y = int(i)


###############
##### LZW #####
###############
def lzw_compression(array):
    dictionary_size = pivot + 1
    maximum_table_size = pow(2, int(16))
    dictionary = {str(k): k for k in range(dictionary_size)}
    compressed_data = []
    string = ''
    for byte in array:
        if string == '':
            string_plus_symbol = str(byte)
        else:
            string_plus_symbol = string + ',' + str(byte)
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if len(dictionary) < maximum_table_size:
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = str(byte)

    if string in dictionary:
        compressed_data.append(dictionary[string])
    return compressed_data


DISTANCES = lzw_compression(distances)
DISTANCES = np.array(DISTANCES, dtype=np.uint16)
DISTANCES.tofile('distances.npy')
t1_stop = process_time()
print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)
