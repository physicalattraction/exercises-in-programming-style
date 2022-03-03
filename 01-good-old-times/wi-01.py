#!/usr/bin/env python
import sys, os, string

# Utility for handling the intermediate 'secondary memory'
def touchopen(filename, *args, **kwargs):
    try:
        os.remove(filename)
    except OSError:
        pass
    open(filename, "a").close() # "touch" file
    return open(filename, *args, **kwargs)


# The constrained memory should have no more than 1024 cells
data = ['']

data.append('')    # data[1] is line (max 80 characters)
data.append(None)  # data[2] is index of the start_char of word
data.append(0)     # data[3] is index on characters, i = 0
data.append(False) # data[4] is flag indicating if word was found
data.append('')    # data[5] is the word
data.append('')    # data[6] is word,p1,p2,...
data.append('')    # data[7] is current word when looping through word index
data.append(1)     # data[8] is current page
data.append(0)     # data[9] is current line page

# Open the secondary memory
word_index = touchopen('word_index', 'rb+')
# Open the input file
f = open(sys.argv[1], 'r')
# Loop over input file's lines
while True:
    data[1] = f.readline()
    if data[1] == '':  # end of input file
        break
    data[2] = None
    data[3] = 0
    # Loop over characters in the line
    while True:
        if data[2] == None:
            if data[1][data[3]].isalnum():
                # We found the start of a word
                data[2] = data[3]
        else:
            if not data[1][data[3]].isalnum():
                # We found the end of a word. Process it
                data[4] = False
                data[5] = data[1][data[2]:data[3]].lower()
                # Let's see if it already exists
                while True:
                    data[6] = str(word_index.readline().strip(), 'utf-8')
                    if data[6] == '':
                        break;
                    # word, no white space
                    data[7] = data[6].split(',')[0].strip()
                    if data[5] == data[7]:
                        data[4] = True
                        break
                if not data[4]:
                    word_index.seek(0, 1)  # Needed in Windows
                    print(f'Empty line becomes "{data[5]},{data[8]}"')
                    word_index.write(bytes(f"{data[5]},{data[8]}\n", 'utf-8'))
                    if data[5] == 'single':
                        raise AssertionError()
                else:
                    print(f'"{data[6]}" becomes "{data[6]},{data[8]}"')
                    word_index.seek(-(len(data[6])), 1)
                    # Note: by overwriting a longer string than what was there, we are overwriting the next word
                    word_index.write(bytes(f"{data[6]},{data[8]}\n", 'utf-8'))
                word_index.seek(0,0)
                # Let's reset
                data[2] = None
        data[3] += 1
        if data[3] == len(data[1]):
            break
