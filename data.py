'''
This file is used to hold the test data for the fillin specs.abs

Once working this file can be replaced with a version that uses a
database.
'''

'''
problem  - is an individual string/paragraphcontaining blanks items.
problemset - is an array of problem items
Data - a dictionary linking each problemset with a unique id
'''

problem1 = [
  {"type":"fillin", "text":"Jack"},
  {"type":"text", "text":" and "},
  {"type":"fillin", "text":"Jill"},
  {"type":"text", "text":" went up the hill."}
]

problem2 = [
  {"type":"text", "text":"Humpty "},
  {"type":"fillin", "text":"Dumpty"},
  {"type":"text", "text":" had a great fall."}
]

problem3 = [
  {"type":"text", "text":"3 x 4 = "},
  {"type":"fillin", "text":"12"}
]

problem4 = [
  {"type":"text", "text":"< "},
  {"type":"fillin", "text":"title"},
  {"type":"text", "text":" > This text appears in the window tab < "},
  {"type":"fillin", "text":"/title"},
  {"type":"text", "text":" >"},
]

problem5 = [
  {"type":"text", "text":"< "},
  {"type":"fillin", "text":"h1"},
  {"type":"text", "text":" > This text appears as the most important heading < "},
  {"type":"fillin", "text":"/h1"},
  {"type":"text", "text":" >"},
]

problem6 = [
  {"type":"text", "text":"< "},
  {"type":"fillin", "text":"b"},
  {"type":"text", "text":" > This text is bold < "},
  {"type":"fillin", "text":"/b"},
  {"type":"text", "text":" >"},
]


problem7 = [
  {"type":"text", "text":"< b > < "},
  {"type":"fillin", "text":"i"},
  {"type":"text", "text":" > This text is bold and italic < "},
  {"type":"fillin", "text":"/i"},
  {"type":"text", "text":" > < "},
  {"type":"fillin", "text":"/b"},
  {"type":"text", "text":" >"},
]


problemsetA = [
  problem1
]

problemsetB = [
  problem1,
  problem2
]

problemsetC = [
  problem1,
  problem2,
  problem3
]

problemsetD = [
  problem2,
  problem3
]

problemsetE = [
  problem4,
  problem5,
  problem6,
  problem7,
  
]

Data = {
  "setA" : problemsetA,
  "setB" : problemsetB,
  "setC" : problemsetC,
  "setD" : problemsetD,
  "setE" : problemsetE
}

import uuid


# get the data related to the unique identifier 
# and create the problem object that can be used
# to render the problem in html

# this function will be changed to get the data from
# the database when this is implemented
def getProblemObj(uid):
  # get the problem specification object format
  # for this uid

  pobj = {} 
  pspec = Data.get(uid)
  pobj["spec"] = pspec
  return pobj


# this function will be changed to save the data to
# the database when this is implemented
def saveProblemObj(pobj):

  # generate a unique id (32char hex string)
  uid = uuid.uuid4().hex

  Data[uid]=pobj["spec"]

  return uid

def getProblemUids():
  uids=[]
  for key in Data:
    uids.append(key)
  return uids




