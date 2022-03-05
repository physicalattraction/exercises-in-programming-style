#!/usr/bin/env python
import sys, re, operator, string

class Stack:
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        return self._stack.pop()

    def peek(self):
        return self._stack[-1]

    def empty(self):
        return len(self._stack) == 0

    def __repr__(self):
        return str(self._stack)

#
# The all-important data stack
#
stack = Stack()

#
# The heap. Maps names to data (i.e. variables)
#
heap = {}

#
# The new "words" (procedures) of our program
#
def read_file():
    """
    Takes a path to a file on the stack and places the entire
    contents of the file back on the stack.
    """
    f = open(stack.pop())
    # Push the result onto the stack
    stack.push([f.read()])
    f.close()

def filter_chars():
    """
    Takes data on the stack and places back a copy with all
    nonalphanumeric chars replaced by white space.
    """
    # This is not in style. RE is too high-level, but using it
    # for doing this fast and short. Push the pattern onto stack
    stack.push(re.compile('[\W_]+'))
    # Push the result onto the stack
    stack.push([stack.pop().sub(' ', stack.pop()[0]).lower()])

def scan():
    """
    Takes a string on the stack and scans for words, placing
    the list of words back on the stack
    """
    # Again, split() is too high-level for this style, but using
    # it for doing this fast and short. Left as exercise.
    heap['words'] = stack.pop()[0].split()
    while len(heap['words']) > 0:
        stack.push(heap['words'].pop())

def remove_stop_words():
    """
    Takes a list of words on the stack and removes stop words.
    """
    f = open('../stop_words.txt')
    stack.push(f.read().split(','))
    f.close()
    # add single-letter words
    stack.push(stack.pop() + list(string.ascii_lowercase))
    heap['stop_words'] = stack.pop()
    # Again, this is too high-level for this style, but using it
    # for doing this fast and short. Left as exercise.
    heap['words'] = []
    while not stack.empty() > 0:
        if stack.peek() in heap['stop_words']:
            stack.pop() # pop it and drop it
        else:
            heap['words'].append(stack.pop()) # pop it, store it
    while len(heap['words']) > 0:
        stack.push(heap['words'].pop())
    del heap['stop_words']; del heap['words']; # Not needed

def frequencies():
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence.
    """
    heap['word_freqs'] = {}
    # A little flavour of the real Forth style here...
    while not stack.empty():
        # ... but the following line is not in style, because the
        # naive implementation would be too slow
        if stack.peek() in heap['word_freqs']:
            # Increment the frequency, postfix style: f 1 +
            stack.push(heap['word_freqs'][stack.peek()]) # push f
            stack.push(1) # push 1
            stack.push(stack.pop() + stack.pop()) # add
        else:
            stack.push(1) # Push 1 in stack[2]
        # Load the updated freq back onto the heap
        heap['word_freqs'][stack.pop()] = stack.pop()

    # Push the result onto the stack
    stack.push(heap['word_freqs'])
    del heap['word_freqs'] # We don't need this variable anymore

def sort():
    # Not in style, left as exercise
    heap['sorted_freqs'] = sorted(stack.pop().items(), key=operator.itemgetter(1), reverse=True)
    while len(heap['sorted_freqs']) > 0:
        stack.push(heap['sorted_freqs'].pop())

def print_freqs():
    stack.push(0)      # number of words printed
    stack.push(False)  # list_empty
    while not stack.pop() and stack.peek() < 25:
        heap['nr_words'] = stack.pop()
        w, f = stack.pop();
        print(w, '-', f)
        heap['list_empty'] = stack.empty()
        stack.push(heap['nr_words']);
        stack.push(1)
        stack.push(stack.pop() + stack.pop())
        stack.push(heap['list_empty'])
    del heap['nr_words']; del heap['list_empty']

# The main function
#
stack.push(sys.argv[1])
read_file(); filter_chars(); scan(); remove_stop_words(); frequencies(); sort(); print_freqs()
