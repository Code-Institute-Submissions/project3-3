from flask import Flask, render_template, request, redirect
import operator
import os
import time
app = Flask(__name__)

# remove passing debug (answer) to render_template on release
highscores = { }

class Player:
    @staticmethod
    def getScores():    # returns a list of tuples with highscores
        return sorted(highscores.items(), reverse = True, key=operator.itemgetter(1))
                
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.question = 0
        self.finished = False # will be set to true upon answering last question
        
    def addPoints(self, number = 5):
        self.score += number
        # since we're adding points, we can as well advance question
        self.question += 1
        if self.question >= len(questions)-1:
            self.finished = True
            
        highscores[self.name] = self.score

        
    def removePoints(self, number = 1):
        self.score -= number
        if self.score < 0:
            self.score = 0
        highscores[self.name] = self.score
        
    def getQandA(self): # returns ('question', 'answer')
        return questions[self.question]
    def getQuestion(self): # returns 'question'
        return questions[self.question][0]
    @classmethod
    def exists(cls, name):
        return name in users
    
questions = [] # ('question', 'answer')
users = { } # 'name' = Player obj

#

def loadQuestions():
    count = 0
    with open('data/questions.txt', 'r') as fp:
        question, answer = '', ''
        for i, line in enumerate(fp):
            line = line.decode("UTF-8").rstrip()
            if i % 2 == 0: # it's a question
                question = line
                count += 1
            else:
                answer = line
                questions.append( (question, answer) )
    return count            
       
totalQuestions = loadQuestions()

print (totalQuestions)
@app.route('/')
def index():
    return render_template('base.html')
    
@app.route('/', methods = ['GET', 'POST'])
def login():
    if ('Username' in request.form):
        username = request.form['Username']
        
        # create a new entry if the user isn't there already
        if not Player.exists(username):
            users[username] = Player(username)

        return redirect(username + '/question')

@app.route('/<username>/question', methods = ['GET', 'POST'])
def game(username):
    player = users[username]
    question, answer = player.getQandA()
    if player.finished:
        return 'THIS IS THE END'
    if ('answer' in request.form):
        print(Player.getScores())
        if answer.lower() in request.form['answer'].lower():
            player.addPoints()
            return render_template('base.html', time = time.time(), scores = Player.getScores(),  count = "[ {0} / {1} ]".format(player.question+1, totalQuestions), username = username, success = True, question = player.getQuestion(), score = player.score)
        else:
            #wrong answer
            player.removePoints()
            return render_template('base.html', debug = answer, time = time.time(), scores = Player.getScores(), count = "[ {0} / {1} ]".format(player.question+1, totalQuestions), wrong_answer = request.form['answer'], username = username, success = False, question = question, score = player.score)
    return render_template('base.html',time = time.time(),  scores = Player.getScores(), firstRound = True, username = username, question = question)
    
@app.route('/<username>', methods = ['GET', 'POST'])
def user(username):
    return render_template('base.html',time = time.time(),  username=username)
    
    
if __name__ == '__main__':
    app.run(host = os.getenv('IP'),
            port = os.getenv('PORT'),
            debug = True)

