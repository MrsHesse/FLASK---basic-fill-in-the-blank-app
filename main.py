from flask import Flask, render_template
from data import Data
app = Flask('app')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer/<uid>')
def answer(uid):

    
    print("uid = ", uid, type(uid))
    pset = Data.get(uid, None)
    print("pset = ", pset)
    
    return render_template('answer_problem.html', pset=pset)

app.run(host='0.0.0.0', port=8080)