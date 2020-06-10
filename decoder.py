from bitarray import bitarray
import numpy as np
from time import process_time

t1_start = process_time()

####################
### reading data ###
####################

# Flags
a = open('flags.npy', 'rb')
flags = bitarray()
flags.fromfile(a)
a.close()

# alphabet
a = open('alphabet.txt', 'r', encoding="utf8")
alphabet = a.read()
alphabet = list(alphabet)
a.close()

# distances
distances = np.fromfile('distances.npy', dtype=np.uint16)

###############
##### LZW #####
###############
pivot = len(alphabet) // 2
dictionary_size = pivot + 1
maximum_table_size = pow(2, int(16))
dictionary = {k: str(k) for k in range(dictionary_size)}
Distances = []
string = ''

for code in distances:
    if not (code in dictionary):
        dictionary[code] = string + ',' + string.split(',')[0]
    i = 0
    x = dictionary[code].split(',')
    while i < len(x):
        Distances.append(int(x[i]))
        i += 1
    if not(len(string) == 0):
        dictionary[dictionary_size] = string + ',' + (dictionary[code].split(',')[0])
        dictionary_size += 1
    string = dictionary[code]


# Restoring data
data = ""
index = -1
pivot = len(alphabet)//2
a = open('decoded.txt', 'w', encoding="utf8")
for i in Distances:
    index += 1
    flag = flags[index]
    if flag:
        a.write(alphabet[pivot - i])
    else:
        a.write(alphabet[pivot + i])

a.close()
t1_stop = process_time()
print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)
