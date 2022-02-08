from flask import Flask, render_template, request, redirect, url_for
from problems import processFillinText

from data import getPage, savePage, getPageUids, flask_create_database,getQuizPage
from datautils import db_isuniquevalue, db_printdicts

app = Flask('app')

@app.route('/')
def index():
    quid = "Q34FgTYaL"
    uids = getPageUids(quid)
    return render_template('index.html', uids=uids)


@app.route('/quiz')
def quiz():
    print("in quiz()")
    print("args -", request.args)

    uid = request.args.get("uid")
    seq = request.args.get("seq",0)

    if not uid:
      print("\tno uid specified so redirecting to getquiz page ")
      return redirect(url_for("getquiz"))
    
    quiz = getQuizPage(uid, seq)

    print("page")
    db_printdicts(quiz["page"])

    print("page spec")
    db_printdicts(quiz["page"]["spec"])

    print("nav")
    print("prev :", quiz["nav"].get("prev"))
    print("next :", quiz["nav"].get("next"))
    

    #pobj = getPage(uid)
    return render_template('answer_page.html', pobj=quiz["page"], nav=quiz["nav"])
    

@app.route('/getquiz', methods=["GET", "POST"])
def getquiz():

  message = ""
  if request.method == "POST":
    # redirect to the homepage
    if request.form.get("cancel"):
      return redirect(url_for("index"))

    print("request.form :", request.form)

    uid = request.form.get("uid")

    if uid:
      # check if the uid exists and rediret to the quiz page using that
      # quiz ID
      if not db_isuniquevalue("quiz", "uid", uid):
        return redirect(url_for("quiz", uid=uid))
      else:
        message = "Code not recognised. Try again "
    else:
      message = "enter a message code"
  
  print("message :", message)
  return render_template("get_code.html", message=message)

@app.route('/answer/<uid>')
def answer(uid):
    pobj = getPage(uid)
    return render_template('answer_page.html', pobj=pobj)

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
        uid = savePage(pobj)
        return redirect(url_for("answer", uid=uid))
    return render_template('enter_page.html', pobj = pobj)


@app.route('/database/create')
def create_database():
  flask_create_database()
  return("database created")


app.run(host='0.0.0.0', port=8080)