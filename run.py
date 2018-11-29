from app.helpers import *



@app.route('/')
def index():
    return render_template('base.html', count = "[ 0 / {0} ]".format(totalQuestions),scores = Player.getScores())
    
@app.route('/', methods = ['GET', 'POST'])
def login():
    if ('Username' in request.form):
        username = request.form['Username']
        
        # create a new entry if the user isn't there already
        if not Player.exists(username) and not username in highscores:
            users[username] = Player(username)
        else:
            return render_template('base.html', error_name = username, count = "[ 0 / {0} ]".format(totalQuestions),scores = Player.getScores())
        return redirect(url_for('game', count = "[ 1 / {0} ]".format(totalQuestions), username = username, scores = Player.getScores()))
        #return redirect(username + '/question')

@app.route('/<username>/question', methods = ['GET', 'POST'])
def game(username):
    player = users[username]
    question, answer = player.getQandA()
    
    if ('answer' in request.form):
        if answer.lower() in request.form['answer'].lower():
            player.addPoints()
            if player.finished:
                return redirect(username + '/finished')
            
            return render_template('base.html', time = time.time(), scores = Player.getScores(),  count = "[ {0} / {1} ]".format(player.question+1, totalQuestions), username = username, success = True, question = player.getQuestion(), score = player.score)
        else:
            #wrong answer
            player.removePoints()
            return render_template('base.html', debug = answer, time = time.time(), scores = Player.getScores(), count = "[ {0} / {1} ]".format(player.question+1, totalQuestions), wrong_answer = request.form['answer'], username = username, success = False, question = question, score = player.score)
    else:
        if 'skip_button' in request.form:
            player.addPoints(0) # just take him to the next round
            question, answer = player.getQandA()
            return render_template('base.html', time = time.time(), scores = Player.getScores(), count = "[ {0} / {1} ]".format(player.question+1, totalQuestions), username = username, success = False, question = question, score = player.score)
    
    return render_template('base.html', count = '[ 1 / {0} ]'.format(totalQuestions), time = time.time(),  scores = Player.getScores(), firstRound = True, username = username, question = question)
    
@app.route('/<username>', methods = ['GET', 'POST'])
def user(username):
    return render_template('base.html', time = time.time(),  username=username)
    

@app.route('/<username>/finished', methods = ['GET'])
def finish(username):
    player = users[username]
    return render_template("finished.html", player = player, scores = Player.getScores())
    
if __name__ == '__main__':
    app.run(host = os.getenv('IP'),
            port = os.getenv('PORT'),
            debug = True)

