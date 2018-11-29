from flask import Flask, render_template, request, redirect, url_for
import operator
import os
import time
import pickle

app = Flask(__name__)


# remove passing debug (answer) to render_template on release
highscores = { }


# save_obj and load_obj are used to save highscores for persistency (doesn't quite work on heroku free plan)

def save_obj(obj, name ):
    with open('data/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

highscores = load_obj('highscores')
    
class Player:
    @staticmethod
    def getScores():    # returns a list of tuples with highscores (first 10)
        return sorted(highscores.items(), reverse = True, key=operator.itemgetter(1))[:10]

                
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.question = 0
        self.finished = False # will be set to true upon answering last question
        
    def addPoints(self, number = 5):
        self.score += number
        save_obj(highscores, 'highscores')
        # since we're adding points, we can as well advance question
        if self.question >= len(questions)-1:
            self.finished = True
        else:
            self.question += 1

            
        highscores[self.name] = self.score

        
    def removePoints(self, number = 1):
        self.score -= number
        if self.score < 0:
            self.score = 0
        highscores[self.name] = self.score
        save_obj(highscores, 'highscores')
        
    def getQandA(self): # returns ('question', 'answer')
        return questions[self.question]
    def getQuestion(self): # returns 'question'
        return questions[self.question][0] or questions[-1][0]
    @classmethod
    def exists(cls, name):
        return name in users
    
questions = [] # ('question', 'answer')
users = { } # 'name' = Player obj

#
with open('data/questions.txt', 'r') as fp:
    question = answer = ''
    for i, line in enumerate(fp):
        line = line.rstrip()
        if i % 2 == 0: # it's a question
            question = line
        else:
            answer = line
            questions.append( (question, answer) )

totalQuestions = len(questions)