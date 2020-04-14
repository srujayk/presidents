import glob

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

import nltk
import heapq
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import gensim
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.spatial import distance
from gensim.models import Word2Vec

speeches = {
    'trump': "",
    "obama": "",
    "gwbush": "",
    "clinton": "",
    "bush": "",
    "reagan": "",
    "carter": ""
}

debates = {
    'trump': "",
    "obama": "",
    "gwbush": "",
    "clinton": "",
    "bush": "",
    "reagan": "",
    "carter": ""
}

all_files = glob.glob("*.txt")

for file in all_files:
    with open(file, "r") as text_file:
        if 'speech' in file:
            score = file.find('_')
            person = file[:score].lower()

            speeches[person] += " "
            speeches[person] += text_file.read()
        else:
            score = file.find('_')
            person = file[:score].lower()

            debates[person] += " "
            debates[person] += text_file.read()

porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def stemSentence(sentence):
    token_words = word_tokenize(sentence)

    updated_stopwords = set(nltk.corpus.stopwords.words('english'))

    tokenized_text = [word for word in token_words if word not in updated_stopwords]

    stem_output = ' '.join([porter.stem(w) for w in tokenized_text])

    return stem_output

def lemSentence(sentence):
    token_words = word_tokenize(sentence)

    updated_stopwords = set(nltk.corpus.stopwords.words('english'))

    tokenized_text = [word for word in token_words if word not in updated_stopwords]

    lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in tokenized_text])

    return lemmatized_output

def get_cosine_sim(str1, str2):

    str1 = lemSentence(str1)
    str2 = lemSentence(str2)

    # sentences to list
    allsentences = [str1 , str2]

    # text to vector
    vectorizer = CountVectorizer()
    all_sentences_to_vector = vectorizer.fit_transform(allsentences)
    text_to_vector_v1 = all_sentences_to_vector.toarray()[0].tolist()
    text_to_vector_v2 = all_sentences_to_vector.toarray()[1].tolist()

    # distance of similarity
    cosine = distance.cosine(text_to_vector_v1, text_to_vector_v2)
    cosine_sim = round((1-cosine), 3)

    return cosine_sim

def get_cosine_tfidf_sim(str1, str2):

    str1 = lemSentence(str1)
    str2 = lemSentence(str2)

    # sentences to list
    allsentences = [str1 , str2]

    # text to vector
    vectorizer = TfidfVectorizer()
    all_sentences_to_vector = vectorizer.fit_transform(allsentences)
    text_to_vector_v1 = all_sentences_to_vector.toarray()[0].tolist()
    text_to_vector_v2 = all_sentences_to_vector.toarray()[1].tolist()

    # distance of similarity
    cosine = distance.cosine(text_to_vector_v1, text_to_vector_v2)
    cosine_sim = round((1-cosine), 3)

    return cosine_sim

print("Cosine Similarity + TFIDF between Trump Speeches and Trump Debates = " + str(get_cosine_tfidf_sim(speeches['trump'], debates['trump'])))
print("Cosine Similarity + TFIDF between Obama Speeches and Obama Debates = " + str(get_cosine_tfidf_sim(speeches['obama'], debates['obama'])))
print("Cosine Similarity + TFIDF between Trump Debates and Obama Debates = " + str(get_cosine_tfidf_sim(debates['obama'], debates['trump'])))
print("Cosine Similarity + TFIDF between Trump Speeches and Obama Speeches = " + str(get_cosine_tfidf_sim(speeches['trump'], speeches['obama'])))
print()
print()
print("Cosine Similarity + TFIDF between Trump Speeches and Trump Debates = " + str(get_cosine_tfidf_sim(speeches['trump'], debates['trump'])))
print("Cosine Similarity + TFIDF between Trump Speeches and Obama Speeches = " + str(get_cosine_tfidf_sim(speeches['trump'], speeches['obama'])))
print("Cosine Similarity + TFIDF between Trump Speeches and GWBush Speeches = " + str(get_cosine_tfidf_sim(speeches['trump'], speeches['gwbush'])))
print("Cosine Similarity + TFIDF between Trump Speeches and Clinton Speeches = " + str(get_cosine_tfidf_sim(speeches['trump'], speeches['clinton'])))
print("Cosine Similarity + TFIDF between Trump Speeches and Bush Speeches = " + str(get_cosine_tfidf_sim(speeches['trump'], speeches['bush'])))
print("Cosine Similarity + TFIDF between Trump Speeches and Reagan Speeches = " + str(get_cosine_tfidf_sim(speeches['trump'], speeches['reagan'])))
print("Cosine Similarity + TFIDF between Trump Speeches and Carter Speeches = " + str(get_cosine_tfidf_sim(speeches['trump'], speeches['carter'])))
print()
print()
print("Cosine Similarity + TFIDF between Obama Speeches and Trump Speeches = " + str(get_cosine_tfidf_sim(speeches['obama'], speeches['trump'])))
print("Cosine Similarity + TFIDF between Obama Speeches and Obama Debates = " + str(get_cosine_tfidf_sim(speeches['obama'], debates['obama'])))
print("Cosine Similarity + TFIDF between Obama Speeches and GWBush Speeches = " + str(get_cosine_tfidf_sim(speeches['obama'], speeches['gwbush'])))
print("Cosine Similarity + TFIDF between Obama Speeches and Clinton Speeches = " + str(get_cosine_tfidf_sim(speeches['obama'], speeches['clinton'])))
print("Cosine Similarity + TFIDF between Obama Speeches and Bush Speeches = " + str(get_cosine_tfidf_sim(speeches['obama'], speeches['bush'])))
print("Cosine Similarity + TFIDF between Obama Speeches and Reagan Speeches = " + str(get_cosine_tfidf_sim(speeches['obama'], speeches['reagan'])))
print("Cosine Similarity + TFIDF between Obama Speeches and Carter Speeches = " + str(get_cosine_tfidf_sim(speeches['obama'], speeches['carter'])))
print()
print()
print("Cosine Similarity + TFIDF between GWBush Speeches and Trump Speeches = " + str(get_cosine_tfidf_sim(speeches['gwbush'], speeches['trump'])))
print("Cosine Similarity + TFIDF between GWBush Speeches and Obama Speeches = " + str(get_cosine_tfidf_sim(speeches['gwbush'], speeches['obama'])))
print("Cosine Similarity + TFIDF between GWBush Speeches and GWBush Debates = " + str(get_cosine_tfidf_sim(speeches['gwbush'], debates['gwbush'])))
print("Cosine Similarity + TFIDF between GWBush Speeches and Clinton Speeches = " + str(get_cosine_tfidf_sim(speeches['gwbush'], speeches['clinton'])))
print("Cosine Similarity + TFIDF between GWBush Speeches and Bush Speeches = " + str(get_cosine_tfidf_sim(speeches['gwbush'], speeches['bush'])))
print("Cosine Similarity + TFIDF between GWBush Speeches and Reagan Speeches = " + str(get_cosine_tfidf_sim(speeches['gwbush'], speeches['reagan'])))
print("Cosine Similarity + TFIDF between GWBush Speeches and Carter Speeches = " + str(get_cosine_tfidf_sim(speeches['gwbush'], speeches['carter'])))
print()
print()
print("Cosine Similarity + TFIDF between Clinton Speeches and Trump Speeches = " + str(get_cosine_tfidf_sim(speeches['clinton'], speeches['trump'])))
print("Cosine Similarity + TFIDF between Clinton Speeches and Obama Speeches = " + str(get_cosine_tfidf_sim(speeches['clinton'], speeches['obama'])))
print("Cosine Similarity + TFIDF between Clinton Speeches and GWBush Speeches = " + str(get_cosine_tfidf_sim(speeches['clinton'], speeches['gwbush'])))
print("Cosine Similarity + TFIDF between Clinton Speeches and Clinton Debates = " + str(get_cosine_tfidf_sim(speeches['clinton'], debates['clinton'])))
print("Cosine Similarity + TFIDF between Clinton Speeches and Bush Speeches = " + str(get_cosine_tfidf_sim(speeches['clinton'], speeches['bush'])))
print("Cosine Similarity + TFIDF between Clinton Speeches and Reagan Speeches = " + str(get_cosine_tfidf_sim(speeches['clinton'], speeches['reagan'])))
print("Cosine Similarity + TFIDF between Clinton Speeches and Carter Speeches = " + str(get_cosine_tfidf_sim(speeches['clinton'], speeches['carter'])))
print()
print()
print("Cosine Similarity + TFIDF between Bush Speeches and Trump Speeches = " + str(get_cosine_tfidf_sim(speeches['bush'], speeches['trump'])))
print("Cosine Similarity + TFIDF between Bush Speeches and Obama Speeches = " + str(get_cosine_tfidf_sim(speeches['bush'], speeches['obama'])))
print("Cosine Similarity + TFIDF between Bush Speeches and GWBush Speeches = " + str(get_cosine_tfidf_sim(speeches['bush'], speeches['gwbush'])))
print("Cosine Similarity + TFIDF between Bush Speeches and Clinton Speeches = " + str(get_cosine_tfidf_sim(speeches['bush'], speeches['clinton'])))
print("Cosine Similarity + TFIDF between Bush Speeches and Bush Debates = " + str(get_cosine_tfidf_sim(speeches['bush'], debates['bush'])))
print("Cosine Similarity + TFIDF between Bush Speeches and Reagan Speeches = " + str(get_cosine_tfidf_sim(speeches['bush'], speeches['reagan'])))
print("Cosine Similarity + TFIDF between Bush Speeches and Carter Speeches = " + str(get_cosine_tfidf_sim(speeches['bush'], speeches['carter'])))
print()
print()
print("Cosine Similarity + TFIDF between Reagan Speeches and Trump Speeches = " + str(get_cosine_tfidf_sim(speeches['reagan'], speeches['trump'])))
print("Cosine Similarity + TFIDF between Reagan Speeches and Obama Speeches = " + str(get_cosine_tfidf_sim(speeches['reagan'], speeches['obama'])))
print("Cosine Similarity + TFIDF between Reagan Speeches and GWBush Speeches = " + str(get_cosine_tfidf_sim(speeches['reagan'], speeches['gwbush'])))
print("Cosine Similarity + TFIDF between Reagan Speeches and Clinton Speeches = " + str(get_cosine_tfidf_sim(speeches['reagan'], speeches['clinton'])))
print("Cosine Similarity + TFIDF between Reagan Speeches and Bush Speeches = " + str(get_cosine_tfidf_sim(speeches['reagan'], speeches['bush'])))
print("Cosine Similarity + TFIDF between Reagan Speeches and Reagan Debates = " + str(get_cosine_tfidf_sim(speeches['reagan'], debates['reagan'])))
print("Cosine Similarity + TFIDF between Reagan Speeches and Carter Speeches = " + str(get_cosine_tfidf_sim(speeches['reagan'], speeches['carter'])))
print()
print()
print("Cosine Similarity + TFIDF between Carter Speeches and Trump Speeches = " + str(get_cosine_tfidf_sim(speeches['carter'], speeches['trump'])))
print("Cosine Similarity + TFIDF between Carter Speeches and Obama Speeches = " + str(get_cosine_tfidf_sim(speeches['carter'], speeches['obama'])))
print("Cosine Similarity + TFIDF between Carter Speeches and GWBush Speeches = " + str(get_cosine_tfidf_sim(speeches['carter'], speeches['gwbush'])))
print("Cosine Similarity + TFIDF between Carter Speeches and Clinton Speeches = " + str(get_cosine_tfidf_sim(speeches['carter'], speeches['clinton'])))
print("Cosine Similarity + TFIDF between Carter Speeches and Bush Speeches = " + str(get_cosine_tfidf_sim(speeches['carter'], speeches['bush'])))
print("Cosine Similarity + TFIDF between Carter Speeches and Reagan Speeches = " + str(get_cosine_tfidf_sim(speeches['carter'], speeches['reagan'])))
print("Cosine Similarity + TFIDF between Carter Speeches and Carter Debates = " + str(get_cosine_tfidf_sim(speeches['carter'], debates['carter'])))
