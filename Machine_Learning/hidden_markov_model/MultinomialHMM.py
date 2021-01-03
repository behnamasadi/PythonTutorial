#get rid of error: Python "SyntaxError: Non-ASCII character '\xe2
# -*- coding: utf-8 -*-
from __future__ import division
import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
  

warnings.filterwarnings("ignore")

############################### Alice and Bob Example ##############################

#https://en.wikipedia.org/wiki/Template:HMM_example

#Alice and Bob, who live far apart from each other and who talk together daily over 
#the telephone about what they did that day. 
#Bob is only interested in three activities: walking in the park, shopping, and cleaning his apartment. 
#The choice of what to do is determined exclusively by the weather. 
#Based on what Bob tells her he did each day, Alice tries to guess what the weather must have been like.

#Pi π 
#start_probability = {'Rainy': 0.6, 'Sunny': 0.4}

#A Matrix (Transition)
#example P(Rainy|Sunny)=0.4
#        Rainy   Sunny
#Rainy   0.7     0.3     sum is 1
#Sunny   0.4     0.6     sum is 1


#B Matrix or Confusion Matrix (Emission)
#P(walk|Rainy)=0.1
#        walk    shop    clean
#Rainy   0.1     0.4     0.5     sum is 1
#Sunny   0.6     0.3     0.1     sum is 1



import numpy as np
from hmmlearn import hmm

states = ["Rainy", "Sunny"]
n_states = len(states)

observations = ["walk", "shop", "clean"]
n_observations = len(observations)

start_probability = np.array([0.6, 0.4])

transition_probability = np.array([
  [0.7, 0.3],
  [0.4, 0.6]
])

emission_probability = np.array([
  [0.1, 0.4, 0.5],
  [0.6, 0.3, 0.1]
])

model = hmm.MultinomialHMM(n_components=n_states)
model.startprob=start_probability
model.transmat=transition_probability
model.emissionprob=emission_probability

# predict a sequence of hidden states based on visible states

#walk    0
#shop    1
#clean   2
#List of activety that bob has done: walk(0), clean(2), shop(1), shop(1), clean(2), walk(0)

bob_says = np.array([[0, 2, 1, 1, 2, 0]]).T
model = model.fit(bob_says)
logprob, alice_guesses = model.decode(bob_says, algorithm="viterbi")
print "Bob says:", ", ".join(map(lambda x: observations[x], bob_says))
print "Alice guesses:", ", ".join(map(lambda x: states[x], alice_guesses))


#model.predict(X, lengths)
#model.predict_proba(X, lengths)
#model.score(X, lengths)

############################### Poker Player Example ##############################



#start_probability = 0.5,0.25,0.25

#A Matrix (transition_probability)
#example P(Honset|Honest)=0.5
#        Honest   Cunning    Lying
#Honest   0.5     0.4        0.1
#Cunning  0.1     0.8        0.1
#Lying    0.1     0.6        0.3

#B Matrix or Confusion Matrix (Emission Matrix)
#P(True|Honest)=0.9
#        True    False
#Honest   0.9     0.1    sum is 1
#Cunning  0.5     0.5    sum is 1
#Lying    0.1     0.9    sum is 1




############################### Dcotor Example ##############################
#https://en.wikipedia.org/wiki/Viterbi_algorithm

#start_probability = 0.5,0.25,0.25

#A Matrix (transition_probability)
#        Healthy   Fever
#Healthy  0.7        0.3
#Fever    0.4        0.6

#B Matrix or Confusion Matrix (Emission Matrix)
#        normal     cold    dizzy
#Healthy  0.5        0.4     0.1
#Fever    0.1        0.3     0.6


############################### Weather Example ##############################

#Initial State Probabilities ( π Vector)
#sunny   0.63
#cloudy  0.17
#rainy   0.20



#A Matrix (transition_probability)
#        sunny   cloudy  rainy
#sunny   0.500   0.250   0.250
#cloudy  0.375   0.125   0.375
#rainy   0.125   0.675   0.375


#B Matrix or Confusion Matrix (Emission Matrix)
#        dry     dryish  damp    soggy
#sunny   0.60    0.20    0.15    0.05
#cloudy  0.25    0.25    0.25    0.25
#rainy   0.05    0.10    0.35    0.50

############################### Dice Example ##############################

#https://de.mathworks.com/help/stats/hidden-markov-models-hmm.html
