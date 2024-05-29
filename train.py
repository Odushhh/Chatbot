# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AWgXxuAzR04_dwb2VtlBZRM-GJ7JFrFh
"""

!pip install tensorflow
!pip install nltk
!pip install flask
!pip install tensorflow

import random
import re
import os
import numpy as np
import pickle
import json
import nltk

from tensorflow.keras.optimizers import SGD
from keras.layers import Dense, Dropout
from keras.models import load_model
from keras.models import Sequential
from nltk.stem import WordNetLemmatizer

#initialize Lemmatizer

lemmatizer = WordNetLemmatizer()
nltk.download('omw-1.4')
nltk.download("punkt")
nltk.download("wordnet")

#intialize files & Load training data

words = []
classes = []
documents = []
ignore_words = ["?", "!", ";", ":"]
data_file = open("intents.json").read()
intents = json.loads(data_file)

#tokenize words -> break down a sentence; each word forms a token

for intent in intents["intents"]:
  for pattern in intent["patterns"]:

    w = nltk.word_tokenize(pattern)
    words.extend(w)

    #add documents
    documents.append((w, intent["tag"]))

    #add classes to main class list
    if intent["tag"] not in classes:
      classes.append(intent["tag"])

#lemmatize words -> reducing words to their base form

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique lemmatized words", words)

pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

#create a Bag of Words -> train model w/ words to recognize patterns

training = []
output_empty = [0] * len(classes)

for doc in documents:
  #initialise BoW
  bag = []

  #list of tokenized words for the pattern
  pattern_words = doc[0]

  #lemmatize each word
  pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

  #create BoW -> indicate 1 if word is found in current pattern
  for w in words:
    bag.append(1) if w in pattern_words else bag.append(0)

    #0 for each tag and 1 for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

  #shuffle features & convert into np.array
  random.shuffle(training)

  #separate BoW represetations & output labels
  train_x = [item[0] for item in training]
  train_y = [item[1] for item in training]

  #convert to NumPy arrays
  train_x = np.array(train_x)
  train_y = np.array(train_y)
  print("Training data created")

#create a model w/ 3 layers;
#layer 1 - 128 neurons
#layer 2 - 64 neurons
#layer 3 - no. of neurons = no. of intents to predict output intent w/ softmax

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))
model.summary()

#compile model

sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

#fitting & saving the model

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save("chatbot_model_v3.h5", hist)
print("Model created")

!pip install torch

from google.colab import drive
drive.mount('/content/drive')

import torch

#connect to Google Drive
from google.colab import drive
drive.mount('/content/drive')

#fitting & saving the model ->> round 2

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('/content/drive/My Drive/ColabModels/chatbot_v3.h5', hist)
print("Model created")

model.summary()

