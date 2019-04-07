from vigenere import encode, decode
import random
import string
import math

alphabet = list(string.ascii_lowercase)
key = 'supersecret'
q = 'beadz'
k_len = 4096 # This is the size of the keyword universe
random.seed(764)

num_injected = int(math.log(k_len, 2))
num_unknown = 100 # number of unknown files
unknown_max = 200 # max size of unknown files
num_queries = 40000 # number of times the user searches

k = [] # This is the keyword universe
files = [] # This is the list of files targeted

# Learned knowledge about the files.
files_knowledge = [[] for _ in range(num_injected + num_unknown)]



# Create our keyword dictionary. Sure, they aren't English.
print("Creating keyword dictionaries.")
for i in range(k_len):
    word = ''
    for i in range(5):
        word += random.choice(alphabet)
    k.append(encode(key, word))


# Create our binary attack files.
# Pattern:
# NYNYNYNY
# NNYYNNYY
# NNNNYYYY
print("Create binary attack files.")
for i in range(num_injected):
    switch_frequency = int(math.pow(2, i))
    switch_on = True
    new_file = []

    for j in range(k_len):
        if j % switch_frequency == 0:
            switch_on = not switch_on

        if switch_on:
            new_file.append(k[j])
    
    files.append(new_file)



# Create the unknown content files.
print("Create unknown content files.")
for i in range(num_unknown):
    new_file = []
    new_file_len = random.randint(1, unknown_max)

    for j in range(new_file_len):
        word = k[random.randint(0, k_len - 1)]
        new_file.append(word)
    files.append(new_file)


def run_query():
    # query = encode(key, q)
    query = k[random.randint(0, k_len - 1)]



    # Run the search query.
    results = []

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

    for i in reversed(range(num_injected)):
        if i in results:
            location += int(math.pow(2, i))

    the_query = k[location] # Will be the same as 'query' above
    the_q = decode(key, k[location])



    # Add to the knowledge about the unknown files.
    for i in range((num_injected), len(files)):
        if i in results:
            if the_q not in files_knowledge[i]:
                files_knowledge[i].append(the_q)



def calc_content_leakage(num_so_far):
    # Now determine how much of the files have been discovered.
    percentages = [0 for _ in range(num_unknown)]
    num_discovered = 0

    for i in range((num_injected), len(files)):
        file_len = len(files[i])
        known_words = len(files_knowledge[i])
        percentage = known_words / file_len
        percentages[i - num_injected] = percentage
        if percentage > 0.9999:
            num_discovered += 1
        # print(str(percentage) + '%')

    total_percentage = sum(percentages) / float(len(percentages))
    # print("Overall: {0:.2f}".format(total_percentage * 100) + '%' + \
    #     " after {} queries.".format(num_so_far))

    # print("{0:.2f}".format(total_percentage * 100))
    print("{}".format(num_discovered / num_unknown * 100))



print("Running queries.")
for i in range(num_queries):
    run_query()
    if ((i + 1) % 200 == 0):
        calc_content_leakage(i + 1)




# print(k[location])
# print(decode(key, k[location]))

# ciphertext = encode(key, 'hello')
# plaintext = decode(key, ciphertext)

# print(ciphertext)
# print(plaintext)