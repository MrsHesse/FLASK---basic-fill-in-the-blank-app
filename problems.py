'''
Contains code for processing and handling the problem data
structures.


'''

'''
Process string containing specification of a fillin problem
and produce the object that is passed to the HTML template to
construct the fillin problems 
'''
# this function splits the input text into lines (using /n)
def processFillinText(text):
  print("in processFillinText() - ", text)
  linearr = text.split("\n")
  parr = []
  perror = []
  pobj = {}
  pobj["spec"]=parr

  # Process each line and create a fillin array.
  # this is then added to an array of sentences.
  # If any of the lines generate and error then an error 
  # message is returned instead of the array 
  linenos=1
  for line in linearr:
    if line:
      p = processFillinLine(line)
      if len(p)>0:
        if p[0]=="ERROR":
          perror.append(f"Line {linenos} - {p[1]}")
        else:
          parr.append(p)
    linenos+=1

  if len(perror)>0:
    pobj["error"]=perror

  return pobj



# process an input string - the assumption is that this
# is a single line from the input
# will return
#   array containing text and fillin objects
#   if there is an error an error message is returned.
#
def processFillinLine(s):
  print("in processFillinLine -", s)
  s = s.strip() + "  "
  fillin = []
  ctype="text"
  cstr="" 
  cerr=None
  
  i=0
  while i < len(s):
    if s[i]=="[" and  s[i+1]=="[":
      # end the previous text and add
      if cstr!="":
        cstr=" " + cstr.strip() + " "
        print("appending text object : " + "-" + cstr + "-" );
        fillin.append({ 
          "type":"text",
          "text":cstr
        })
  
      # start of a fillin
      i=i+2;
      cstr=s[i];
      ctype="fillin";
    elif s[i]=="]" and s[i+1]=="]":
      # end of fillin
      i=i+1;
      cstr=" " + cstr.strip() + " "
      print("appending fillin object : " + "-" + cstr + "-" );
      fillin.append({ 
        "type":"fillin",
        "text":cstr
        })

      ctype="text"
      cstr=""
    else:
      # just text - add to the current string
      cstr+=s[i]

    i+=1
  
  if (ctype=="text"):
    cstr+=s[-1]

    cstr = cstr.strip()

    if cstr!="":
      cstr = " " + cstr
      print("appending last text object : " + "-" + cstr + "-" );
      fillin.append({ 
            "type":"text",
            "text":cstr
          })
  elif (ctype=="fillin"):
    cerr = "blank not ended - missing ]]"

  if cerr:
    fillin = ["ERROR", cerr]
  
  return fillin

