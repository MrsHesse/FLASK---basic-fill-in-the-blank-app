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
