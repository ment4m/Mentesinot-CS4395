import re
from nltk import word_tokenize
import pickle


# Build separate language model for 3 languages
# Create a function with a file name as argument
def processFile(fileRawText):
    # Read in the text, remove newlines
    text = re.sub(r'[.?!,:;()\-\'\"\d]', ' ', fileRawText.lower())

    # Tokenize the text
    unigrams = word_tokenize(text)

    # Use nltk to create a bigrams list
    bigramsList = [(unigrams[k], unigrams[k + 1]) for k in range(len(unigrams) - 1)]

    # Create a unigrams list using nltk
    unigramsList = list(unigrams)

    # Use the bigram list to create a bigram dictionary of bigrams and counts
    bigramDict = {b: bigramsList.count(b) for b in set(bigramsList)}

    # Use the unigram list to create a unigram dictionary of unigrams and counts
    unigramDict = {t: unigramsList.count(t) for t in set(unigramsList)}

    # Return the unigram dictionary and bigram dictionary from the function
    return unigramDict, bigramDict


# Main function
if __name__ == '__main__':
    # Read each of the three files and store them as raw text
    with open('LangId.train.English', 'r') as f:
        englishFile = f.read()
    f.close()
    with open('LangId.train.French', encoding="utf8") as f:
        frenchFile = f.read()
    f.close()
    with open('LangId.train.Italian', encoding="utf8") as f:
        italianFile = f.read()
    f.close()

    # pickle the english unigram and bigram dictionaries
    englishUnigramDict, englishBigramDict = processFile(englishFile)
    pickle.dump(englishUnigramDict, open('englishUnigram.pik', 'wb'))
    pickle.dump(englishBigramDict, open('englishBigram.pik', 'wb'))

    # pickle the french unigram and bigram dictionaries
    frenchUnigramDict, frenchBigramDict = processFile(frenchFile)
    pickle.dump(frenchUnigramDict, open('frenchUnigram.pik', 'wb'))
    pickle.dump(frenchBigramDict, open('frenchBigram.pik', 'wb'))

    # pickle the italian unigram and bigram dictionaries
    italianUnigramDict, italianBigramDict = processFile(italianFile)
    pickle.dump(italianUnigramDict, open('italianUnigram.pik', 'wb'))
    pickle.dump(italianBigramDict, open('italianBigram.pik', 'wb'))

    print('\nProgram training is ended')
