from myre import *
import sys

filename = sys.argv[1]
s = sys.argv[2]
# print(filename, s)
s = preprocess(s)
nfa = re2nfa(s)
dfa = nfa.toDFA()
dfa.toGraph()

with open(filename, 'r') as f:
    text = f.read().lower()
    text = text.replace(',', '')
    text = text.replace('"', '')
    text = text.replace('.', '')
    text = text.replace("'", '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    words = text.split(' ')

for word in words:
    # print(word, nfa.match(word))
    if nfa.match(word):
        print(word)

# nfa.toGraph()