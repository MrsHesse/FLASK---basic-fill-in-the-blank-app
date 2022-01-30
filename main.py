from flask import Flask, render_template, request
from problems import processFillinText

import json
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

@app.route('/enter', methods=["GET", "POST"])
def enter():
    pobj=None
    
    if request.method=="POST":
      # we need to process the textarea and create object
      # that can be used to create a fill in the blank problem
      text = request.form.get("problem-text")

      print("in enter. text =", text)
      pobj = processFillinText(text)
      pobj["message"] = [pobj.get("error","valid specification")]
      pobj["text"]=text

      print("mesage :[",len(pobj["message"]),"]", pobj["message"])


    return render_template('enter_problem.html', pobj = pobj)

#    return render_template('enter_problem.html', pspec=pspec, message=message)


'''
# the client can post new data to add to the database
# via the /json route
@app.route("/json", methods=["POST"])
def receivejson():
  # Validate the request body contains JSON
  if request.is_json:
    # Parse the JSON into a Python dictionary
      req = request.get_json()

      # Print the dictionary
      print(req)
      
      with open('file.json', 'w') as f:
        json.dump(req, f)
      
      # Return a string along with an HTTP status code
      return "JSON received!", 200

  else:

      # The request body wasn't JSON so return a 400 HTTP status code
      return "Request was not JSON", 400
'''
app.run(host='0.0.0.0', port=8080)