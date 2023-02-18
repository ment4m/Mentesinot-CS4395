import sys # for reading and exiting from file and program
import nltk # word_tokenize, WordNetLemmatizer, stopwords, and pos_tag functions
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import random


# preprocessing Function to preprocess the raw text
def processing(text):
    # Tokenize the lowercase the text
    tokens = word_tokenize(text.lower())

    # Store the stopwords
    stop_words =set(stopwords.words('english'))

    # of the unique token choose the ones that are greater than 5, alpha and not stopwords
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words and len(t) > 5]

    # Lemmatize the tokens and use set() to make a list of unique lemmas
    unique_lemmas = sorted(list(set([WordNetLemmatizer().lemmatize(r) for r in tokens])))

    # use POS tagging on the unique lemmas and print the first 20 tagged items
    lemmas_unique_tags = nltk.pos_tag(unique_lemmas)

    # Create a list of only those lemmas that are nouns
    noun_lemmas = list([x[0] for x in lemmas_unique_tags if x[1].startswith("N")])

    # Print the len of tokens and the len of nouns after preprocessing
    # Calculate the lexical diversity of the tokenized text and output it
    print("Lexical diversity: %.2f" % (len(unique_lemmas) / (len(tokens))))
    print('\nFirst 20 Tagged Words:', lemmas_unique_tags[:20])
    print('\nlen of tokens after preprocessing ', len(tokens))
    print('len of noun after preprocessing ', len(noun_lemmas))

    return tokens, noun_lemmas


# Guessing game function
def guessing_game(nouns):
    # Start with guess number 5
    guess_num = 5

    # select randomly choose from the top 50
    random_word_select = random.choice(nouns)[0]
    right_word = []
    guessed_letter = []

    # start the game
    print("\nLet's play a word guessing game!")

    # print the _ and space
    for element in random_word_select:
        print('_', end=" ")

    # the game stop when guess_num is negative
    while guess_num > -1:
        letter_input = input('\nGuess a letter: ').lower()

        # Prompt the user to input a valid value
        if not letter_input.isalpha() and letter_input != "!":
            print("\nType a valid letter, please!")

        # Prompt the user to retry if they entered a guessed letter
        elif letter_input in guessed_letter:
            print("You have already tried it, try again!")

        # The game ends when the user enters ‘!’
        elif letter_input != "!":
            # Populate a list that holds all user guesses
            guessed_letter.append(letter_input)

            # If the letter is right, fill in all matching letter _ with the letter and add 1 point to the guess_num
            if letter_input in random_word_select:
                guess_num += 1
                right_word.append(letter_input)
                # give the score
                print("Right! Score is ", guess_num)

            # If the letter is not in the word, subtract 1 from the guess_num and print message
            else:
                guess_num -= 1
                # give the score
                print("Sorry, guess again. Score is ", guess_num)

            # Update and print the current state of the game
            count = 0
            for element in random_word_select:
                if element in right_word:
                    print(element, end=" ")
                    count += 1
                else:
                    print('_', end=" ")

            # if the user guesses the word correctly, game over
            if count == len(random_word_select):
                print("\nYou solver it!")
                # prompt the user if you want to play again
                decision_play_again = input("\nDo you want to Play again? (Y/N) ")
                if decision_play_again.lower() == "y":
                    guessing_game(nouns)
                else:
                    print("\nThank you for playing!")
                    sys.exit(0)

        else:
            print("\nThank you for playing!")
            sys.exit(0)

    # Keep a cumulative total score and end the game if it is negative
    print("\n\nYou lost by score")
    print("The word was:", random_word_select)

    # prompt the user if they want to play again
    decision_play_again = input("\nDo you want to Play again? (Y/N) ")
    if decision_play_again.lower() == "y":
        guessing_game(nouns)
    else:
        print("\nThank you for playing!")
        sys.exit(0)


if __name__ == '__main__':
    # Send the filename to the main program in a system argument.
    # If no system arg is present, print an error message and exit the program.
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print('Input file: ', input_file)

        with open('anat19.txt', 'r') as f:
            raw_text = f.read()

        tokens, noun_lemmas = processing(raw_text)
        common_list = []

        # Dictionary of {noun:count of noun in tokens} items from the nouns and tokens lists
        counts = {t: tokens.count(t) for t in noun_lemmas}

        # Sort the dictionary by count and print the 50 most common words and their counts
        # Save these words to a list because they will be used in the guessing game
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        print("\n50 most common words:")
        for i in range(50):
            common_list.append(sorted_counts[i])
            print(sorted_counts[i])

        # Start a guessing game with the list of 50 words
        guessing_game(common_list)
    else:
        print('Please enter a filename as a system arg')