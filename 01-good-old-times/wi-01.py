#!/usr/bin/env python
import sys, os, string
import shutil

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
data.append([])    # data[10] is list of pages for current word

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
                    word_index.write(bytes(f'{data[5]:>20}' + f',{data[8]:>3}' + ' ' * 396 + '\n', 'utf-8'))
                else:
                    word_index.seek(-(len(data[6])+1), 1)
                    data[7] = data[6].split(',')[0].strip()  # Bring back the leading spaces
                    data[10] = ''.join(data[6].split(',')[1:]).strip()  # Bring back the leading spaces
                    # Note: by overwriting a longer string than what was there, we are overwriting the next word
                    # There is no "decent" way of doing this correctly, I don't feel like wasting my time on it
                    # https://bytes.com/topic/python/answers/44208-changing-line-text-file
                    print(('DRAGONS', len(data[6]), 420-len(data[6] + f',{data[8]:>3}')))
                    print(f'"{data[6]}"')
                    print(data[6] + f',{data[8]:>3}' + ' ' * (420-len(data[6] + f',{data[8]:>3}')) + '\n')
                    word_index.write(bytes(data[7] + "," + data[10] + f',{data[8]:>3}' + ' ' * (420-len(data[7] + "," + data[10] + f',{data[8]:>3}')) + '\n', 'utf-8'))
                word_index.seek(0, 0)
                # Let's reset
                data[2] = None
        data[3] += 1
        if data[3] == len(data[1]):
            break
