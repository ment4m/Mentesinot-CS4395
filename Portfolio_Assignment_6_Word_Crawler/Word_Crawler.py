# Mentesinot Cherenet
# CS 4395.001
# Professor Karen Mazidi
# March 11, 2023

from urllib import request
from bs4 import BeautifulSoup
import requests
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from collections import defaultdict
import pickle


def web_crawler(starter_url):
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    # create a list of URLs
    list_of_urls = []

    counter = 0
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if 'michael' in link_str or 'Michael' in link_str or 'Jordan' in link_str or 'jordan' in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('https') \
                    and 'google' not in link_str \
                    and 'facebook' not in link_str \
                    and 'twitter' not in link_str \
                    and 'instagram' not in link_str \
                    and link_str not in list_of_urls:
                # add URL to the list
                list_of_urls.append(link_str)
                print(link_str)
                if counter == 14:
                    break
                counter += 1

    return list_of_urls


def web_scraper(list_of_urls, raw_text_files):
    for i in range(len(list_of_urls)):

        url = list_of_urls[i]
        html = request.urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(html, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        text = soup.get_text()

        f = open(raw_text_files[i], 'w', encoding="utf-8")

        # write text to file
        f.write(text)
        f.close()


def text_cleaner(raw_text_files, cleaned_text_files):
    for i in range(len(raw_text_files)):
        f = open(raw_text_files[i], 'r', encoding="utf-8")
        raw_text = f.read()
        f.close()

        cleaned_text = ' '.join(raw_text.split())

        f = open(cleaned_text_files[i], 'w', encoding="utf-8")

        sentences = sent_tokenize(cleaned_text)
        for sentence in sentences:
            f.write(sentence + "\n")

        f.close()


def extract_tokens(cleaned_text_files):
    text = ""
    for i in range(len(cleaned_text_files)):
        f = open(cleaned_text_files[i], 'r', encoding="utf-8")
        text += f.read()
        f.close()

    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [w.lower() for w in words if w.lower() not in stopwords.words('english') and (w.isalpha() or w.isnumeric())]
    frequency = dict(Counter(words))
    frequency = dict(reversed(sorted(frequency.items(), key=lambda item: item[1])))

    words = []
    for i in frequency:
        if len(words) == 40:
            break
        words.append(i)

    return sentences, words


def searchable_knowledgebase(words, sentences):
    knowledgeBase = defaultdict(str)
    for sentence in sentences:
        for word in words:
            # if the word is in the sentence add to knowledge base
            if word in sentence.lower():
                knowledgeBase[word] += " " + sentence
    return knowledgeBase


if __name__ == '__main__':

    starterUrl = "https://en.wikipedia.org/wiki/Michael_Jordan"
    print("starter website " + starterUrl)
    print("15 Relevant websites:")
    listOfUrls = web_crawler(starterUrl)

    rawFiles = []
    cleanedFiles = []

    # generate file names
    for i in range(len(listOfUrls)):
        rawFiles.append("rawText" + str(i + 1) + ".txt")
        cleanedFiles.append("cleanedText" + str(i + 1) + ".txt")

    web_scraper(listOfUrls, rawFiles)
    print("Scraped text ...")

    text_cleaner(rawFiles, cleanedFiles)
    print("Cleaned up the text ...")

    sentences, words = extract_tokens(cleanedFiles)
    print("Top 40 words on websites " + str(words))

    knowledgeBase = ["jordan", "michael", "nba", "bulls", "per", "basketball", "mvp", "player", "wizards", 'chicago']

    knowledge = searchable_knowledgebase(knowledgeBase, sentences)

