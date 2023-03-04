import pickle
from nltk import word_tokenize, ngrams


# This function will calculate the probability of each language used per line
def computeProb(line, unigram, bigram, V):
    p_laplace = 1
    unigramsTokens = word_tokenize(line)
    bigramsList = list(ngrams(unigramsTokens, 2))

    # b is the bigram count
    # u is the unigram count
    # v is the total vocabulary size
    for big in bigramsList:
        b = bigram[big] if big in bigram else 0
        u = unigram[big[0]] if big[0] in unigram else 0
        p_laplace = p_laplace * ((b + 1) / (u + V))

    return p_laplace


# Main function
if __name__ == '__main__':

    # Read the pickled dictionaries created in program 1
    englishUnigram = pickle.load(open('englishUnigram.pik', 'rb'))
    englishBigram = pickle.load(open('englishBigram.pik', 'rb'))

    frenchUnigram = pickle.load(open('frenchUnigram.pik', 'rb'))
    frenchBigram = pickle.load(open('frenchBigram.pik', 'rb'))

    italianUnigram = pickle.load(open('italianUnigram.pik', 'rb'))
    italianBigram = pickle.load(open('italianBigram.pik', 'rb'))

    # Get the total length of all three unigrams
    V = len(englishUnigram) + len(frenchUnigram) + len(italianUnigram)

    # Open the test file and append each line to a list
    with open('LangId.test', 'r') as f:
        test_file = f.readlines()
    f.close()

    # Open the actual solution and append each each line to a list
    with open('LangId.sol', 'r') as f:
        actualSolution = f.readlines()
    f.close()

    # Create/Write a new file to store our predicted solution
    f = open("PredictedSolutionFile.txt", "w")
    f.close()

    # These values are to be used later in the program
    predictedSolution = []
    wrongLines = []
    correctCount = 0
    lineNumber = 0

    # For each test file, calculate the probability for each language and write the
    # language with the highest probability to a file.
    for line in test_file:
        lineNumber += 1

        englishProb = computeProb(line, englishUnigram, englishBigram, V)
        frenchProb = computeProb(line, frenchUnigram, frenchBigram, V)
        italianProb = computeProb(line, italianUnigram, italianBigram, V)

        # Write the language with the highest probability to the "PredictedSolutionFile.txt" file
        if englishProb > frenchProb and englishProb > italianProb:
            with open('PredictedSolutionFile.txt', 'a') as f:
                f.write(str(lineNumber) + " English\n")
            f.close()

        elif frenchProb > englishProb and frenchProb > italianProb:
            with open('PredictedSolutionFile.txt', 'a') as f:
                f.write(str(lineNumber) + " French\n")
            f.close()

        else:
            with open('PredictedSolutionFile.txt', 'a') as f:
                f.write(str(lineNumber) + " Italian\n")
            f.close()

    # Open the predicted solution file and append each line to a list
    with open('PredictedSolutionFile.txt', 'r') as f:
        predictedSolution = f.readlines()
    f.close()

    # This compares the actual solution to our predicted solution
    for i in range(len(predictedSolution)):
        if predictedSolution[i] == actualSolution[i]:
            correctCount += 1
        else:
            wrongLines.append(i + 1)

    # Calculate and print number of correct lines, total number of lines,
    # the predicted accuracy, and the lines that were categorized incorrectly
    accuracy = correctCount / len(predictedSolution)
    print("Number of correct lines:", correctCount)
    print("Total lines:", len(predictedSolution))
    print("Accuracy:", '%.2f' % accuracy)
    print("Incorrect lines:", wrongLines)