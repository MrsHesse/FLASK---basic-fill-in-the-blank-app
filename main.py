from flask import Flask, render_template, request, redirect, url_for
from problems import processFillinText

from data import getProblemObj, saveProblemObj, getProblemUids

app = Flask('app')

@app.route('/')
def index():
    uids = getProblemUids()
    return render_template('index.html', uids=uids)

@app.route('/answer/<uid>')
def answer(uid):
    pobj = getProblemObj(uid)
    return render_template('answer_problem.html', pobj=pobj)

@app.route('/enter', methods=["GET", "POST"])
def enter():
    pobj=None
    
    if request.method=="POST":
      # we need to process the textarea and create object
      # that can be used to create a fill in the blank problem
      text = request.form.get("problem-text")

      # set up the pobj object
      pobj = processFillinText(text)
      pobj["message"] = [pobj.get("error","valid specification")]
      pobj["error"] = pobj.get("error")
      pobj["text"]=text

      # if the generate button is pressed 
      #     save the problem to the database
      #     get the uid
      #     redirect to the answer route using this uid
      if "generate" in request.form:
        uid = saveProblemObj(pobj)
        return redirect(url_for("answer", uid=uid))
    return render_template('enter_problem.html', pobj = pobj)


app.run(host='0.0.0.0', port=8080)