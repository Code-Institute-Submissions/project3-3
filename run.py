from flask import Flask, render_template, request

import os

app = Flask(__name__)
users = { }

@app.route('/')

def index():
    return render_template('base.html')
    
@app.route('/', methods = ['POST'])
def user():
    print (request.form['Username'])
    return render_template('base.html', username = request.form['Username'])

def about():
    return 'about us'
    

if __name__ == '__main__':
    app.run(host = os.getenv('IP'),
            port = os.getenv('PORT'),
            debug = True)

