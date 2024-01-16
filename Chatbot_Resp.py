import json
import random
import warnings

import nltk
import numpy
from keras.models import load_model
from nltk.stem import WordNetLemmatizer

warnings.filterwarnings("ignore")

lemmatizer = WordNetLemmatizer()
model = load_model("Chatbot_Model.h5")

intents = {}
words = {}
classes = {}
Documents = {}

with open("intents.json") as f:
    intents = json.load(f)

with open("words.json") as f:
    words = json.load(f)

with open("classes.json") as f:
    classes = json.load(f)

with open("documents.json") as f:
    documents = json.load(f)


def sentence_in_words(sentence):
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in nltk.word_tokenize(sentence)]

    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return (numpy.array(bag))


def predicting_intent(sentence):
    bag = sentence_in_words(sentence)
    res = model.predict(numpy.array([bag]))[0]

    results = [[i, r] for i, r in enumerate(res)]
    results.sort(key=lambda x: x[1], reverse=True)

    if (results[0][0] < 0.50):
        results = [{"intent": 'i do not understand',
                    "probability": str(results[0][1])}]
    else:
        results = [{"intent": classes[results[0][0]],
                    "probability": str(results[0][1])}]
    return results


def get_Response(ints):
    tag = ints[0]['intent']
    for i in intents['intents']:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            return result


def chatbot_response(msg):
    ints = predicting_intent(msg)
    response = get_Response(ints)
    return response
