import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP NP
S -> NP VP
S -> VP NP PP
S -> VP P NP Conj VP
S -> VP PP
S -> VP NP Conj VP PP Adv
S -> VP Conj NP
S -> VP NP PP Conj VP PP
S -> VP Det Adj NP PP PP

NP -> N | Det N | Det Adj N | V Det N
VP -> V | N V | V N | N Adv V | N V Adv
PP -> P | P N | P Det N | P Det Adj N
Adj -> Adj | Adj Adj | Adj Adj Adj
"""
# 10: N V Det Adj Adj Adj N P Det N P Det N
#     VP  Det Adj         NP PP     PP 
 
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Remove dots
    sentence = sentence.replace('.', '')
    
    # Split words
    sentence_list = sentence.split()
    
    # print(f'sentence list: {sentence_list}')
    array = []

    # Loop over words
    for sentence in sentence_list:
        # Check letters in words. If there is at least one alphabetic letter, we consider as word.
        for letter in sentence:
            if letter.isalpha():
                array.append(sentence.lower())
                break
    # print("list of sentence")
    # print(array)
    return array

#a = preprocess("My companion smiled an enigmatical smile.")

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    # Convert Tree to Parented Tree
    ptree = nltk.tree.ParentedTree.convert(tree)

    # print(f'ptrees subtrees: {ptree}')
    # Iterate through all subtrees in the tree:
    for subtree in ptree.subtrees():

        # If subtree is labelled as a noun then parent is a noun phrase chunk
        if subtree.label() == "N":
            chunks.append(subtree.parent())

    return chunks

if __name__ == "__main__":
    main()
