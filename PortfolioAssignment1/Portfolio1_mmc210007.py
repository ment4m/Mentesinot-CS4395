import sys  # to get the system parameter
import os
import re   # used for regular expressions
import pickle

# Description: This program work the Text Processing with Python
# Class: CS: 4395.001 Human Language Technology
# Portfolio2: WorldGame
# Date: 02/04/2023
# @author  Mentesinot Cherenet
# @version 1.0.0

# Define a Person class
# Contains inti method and display method
class Person:
    # display method class with fields: last, first, mi, id, and phone
    def __init__(input, last, first, mi, id, phone):
        input.last = last
        input.first = first
        input.mi = mi
        input.id = id
        input.phone = phone
    # display() method to output fields as shown in the sample run
    def display(input):
        print("Employee id:", input.id)
        print("\t    ", input.first, input.mi, input.last)
        print("\t    ", input.phone)

# Function to read a file
# @returns a text which is of type string
def readFile(fp):
    with open(os.path.join(os.getcwd(), fp), 'r') as f:
        textFile = f.read()
    return textFile

# Function to process a text
# returns a dictionary of person objects
def processText(text):
    dict = {}
    # read each all sentences from the file
    sentences = text.split('\n')
    # The for loop to iterate each sentences
    for sentence in sentences[1:]:   # [1:] to ignore the first sentence which is the Heading line
        
        # get all informations from person object which is split on comma to get the fields as text variables
        tokens = sentence.split(',')
        
        # change the first name capital case for last name and the first name
        lName = tokens[0][0].upper() + tokens[0][1:].lower()
        fName = tokens[1][0].upper() + tokens[1][1:].lower()
        
        # check the middle name character
        # if the middle intial is not present set to X else use make is upper case
        mid = tokens[2].upper() if tokens[2] != '' else 'X'
        
        # read the ID
        pId = tokens[3]
        
        # check the pattern of ID which is 2 letters followed by 4 numbers
        # if the pattern was not matched, prompt the user to put the valid input "aa1234" or "AA1234"
        patternMatched = re.search("[a-zA-Z]{2}[0-9]{4}", pId)
        while not patternMatched:
            print("ID invalid:", pId)
            print("ID is two letters followed by 4 digits")
            pId = input("Please enter a valid id: ")
            patternMatched = re.search("[a-zA-Z]{2}[0-9]{4}", pId)
            
        # check if the number is of the format 123-456-7890
        # if the pattern was not matched, prompt the user to put the valid input "123-456-7890"
        phoneNumber = tokens[4]
        phoneNumberMatched = re.search("([0-9]{3})-([0-9]{3})-([0-9]{4})", phoneNumber) 
        while not phoneNumberMatched:
            print(f"Phone {phoneNumber} is invalid")
            print("Enter phone number in the form 123-456-7890")
            phoneNumber = input("Enter phone number: ")
            phoneNumberMatched = re.search("([0-9]{3})-([0-9]{3})-([0-9]{4})", phoneNumber)
            
        # create the person object
        person = Person(lName, fName, mid, pId, phoneNumber)
        # check if the personID already exist in the dictionary
        if pId in dict:
            print(f"{pId} already exists!")
        else:
            dict[pId] = person
    return dict

 # main function contains
 # Save the dictionary as a pickle file
 # Open the pickle file for read
 # print each person using the Person display() method
if __name__ == '__main__':
    # Check if system arg has less than the required argument
    if len(sys.argv) < 2:
        print('Error: Please enter a filename as a system arg')
    else:
        # read the filename argument to  inputfile
        inputFile = sys.argv[1]
        # call a function readFile to convert the input file to of type string
        readText = readFile(inputFile)
        dict = processText(readText)
        # save the directionary as a pickle file
        pickle.dump(dict, open('dict.p', 'wb'))
        # open the pickle file for read
        dict_in = pickle.load(open('dict.p', 'rb'))
        print("Employee list:\n")
        # display each person object in the dictionary
        for person in dict_in.values():
            person.display()
            print()
