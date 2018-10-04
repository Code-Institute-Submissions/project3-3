from flask import Flask, render_template, request, redirect

import os

app = Flask(__name__)

# list of tuples, going to load questions into it from a file later
questions = [
        ('What is what?', 'i dunno'),
        ("How are you?", 'Good'),
        ("Capital of france?", "Paris")
    ]

#
scores = { }
def get_next_question(user):
    return questions[scores[user]['question']]
    
def getScore(user):
    return scores[user]['score']
    
def check_answer(user, answer):
    q = get_next_question(user)
    
    if q[1].lower() == answer.lower():
        scores[user]['score'] += 2
        print ('score for user: ' + user + ' : ' + str(scores[user]['score']))
        return q[1]
    else:
        # write down invalid answer to a div below
        print(answer)
        return False   
    # up the round number anyway

@app.route('/')
def index():
    return render_template('base.html')
    
@app.route('/', methods = ['GET', 'POST'])
def login():
    if ('Username' in request.form):
        username = request.form['Username']
        
        # create a new entry if the user isn't there already
        if not username in scores:
            scores[username] = { 'question': 0, 'score': 0, 'answer': questions[0][1] }
        return redirect(username + '/question')

@app.route('/<username>/question', methods = ['GET', 'POST'])
def game(username):
    question, answer = get_next_question(username)
    if ('answer' in request.form):
        if answer.lower() == request.form['answer'].lower():
            scores[username]['question'] += 1
            scores[username]['score'] += 1
            question = get_next_question(username)[0]
            return render_template('base.html', username = username, success = True, question = question, score = getScore(username))
        else:
            #wrong answer
            return render_template('base.html', wrong_answer = request.form['answer'], username = username, success = False, question = question, score = getScore(username))
    return render_template('base.html', firstRound = True, username = username, question = question)
    
@app.route('/<username>', methods = ['GET', 'POST'])
def user(username):

    #probably need to add a tuple with question/answer to render_template
    return render_template('base.html', username=username)
    
    
if __name__ == '__main__':
    app.run(host = os.getenv('IP'),
            port = os.getenv('PORT'),
            debug = True)

