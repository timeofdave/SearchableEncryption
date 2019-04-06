from vigenere import encode, decode
import random
import string
import math

alphabet = list(string.ascii_lowercase)
key = 'supersecret'
q = 'beadz'
k_len = 4096 # This is the size of the keyword universe
random.seed(43)

k = [] # This is the keyword universe
files = [] # This is the list of files targeted

# Create our keyword dictionary. Sure, they aren't English.
for i in range(k_len):
    word = ''
    for i in range(5):
        word += random.choice(alphabet)
    k.append(word)


# Create our binary attack files.
# Pattern:
# NYNYNYNY
# NNYYNNYY
# NNNNYYYY
for i in range(int(math.log(k_len, 2))):
    switch_frequency = int(math.pow(2, i))
    switch_on = True
    new_file = []

    for j in range(k_len):
        if j % switch_frequency == 0:
            switch_on = not switch_on

        if switch_on:
            new_file.append(k[j])
    
    files.append(new_file)
        

# Run the search query.
results = []
query = q # defined in the constants

for i in range(len(files)):
    found = False

    for j in range(len(files[i])):
        if files[i][j] == query:
            found = True
    
    if found:
        results.append(i)


# Determine which word it was.
# Starts out with a range of size k_len.
# Ends with a single word.
# Range always begins at 'location'.
location = 0

for i in reversed(range(int(math.log(k_len, 2)))):
    if i in results:
        location += int(math.pow(2, i))




print(k[location])

# ciphertext = encode(key, 'hello')
# plaintext = decode(key, ciphertext)

# print(ciphertext)
# print(plaintext)