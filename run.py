from flask import Flask
import os

app = Flask(__name__)

@app.route('/')

def index():
    return "Hello world"
    
@app.route('/about')

def about():
    return 'about us'
    
if __name__ == '__main__':
    app.run(
            host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=True
            )

