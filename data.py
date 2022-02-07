
from datautils import db_setname, db_connect, db_cursor, db_tables, db_print_table, db_table_exists, db_getrecords, db_getrecord, db_getdicts, db_printrecords, db_printdicts, db_isuniquevalue, db_getunique

import json


db_setname("problems.db")


'''
This file is used to access and manage the databases used in the app

'''

'''
functions for creating the database and tables for this project 
'''
def createDatabase():

  print("in createDatabase()")
  conn = db_connect()

  # remove previous versions of each table 
  # and create a new version of the table

  # create users table
  if db_table_exists(conn, "users"):
    conn.execute('DROP TABLE users;')

  user_schema = """
      CREATE TABLE users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        password text
      );
      """
  conn.execute(user_schema);
  print("created user table")

  # create quiz table
  if db_table_exists(conn, "quiz"):
    conn.execute('DROP TABLE quiz;')

  schema = """
      CREATE TABLE quiz (
        quizid INTEGER PRIMARY KEY,
        uid TEXT,
        title TEXT,
        details text
      );
      """
  conn.execute(schema);
  print("created quiz table")


  # create page table
  if db_table_exists(conn, "page"):
    conn.execute('DROP TABLE page;')

  schema = """
      CREATE TABLE page (
        pageid INTEGER PRIMARY KEY,
        uid TEXT,
        title TEXT,
        details text,
        spec TEXT
      );
      """
  conn.execute(schema);
  print("created page table")


  # create quizcontent table
  if db_table_exists(conn, "quizcontent"):
    conn.execute('DROP TABLE quizcontent;')

  schema = """
      CREATE TABLE quizcontent (
        quizuid TEXT,
        pageuid TEXT,
        seq INTEGER
      );
      """
  conn.execute(schema);
  print("created quiz quizcontent")
  

  # create user table
  if db_table_exists(conn, "user"):
    conn.execute('DROP TABLE user;')

  schema = """
      CREATE TABLE user (
        name TEXT,
        password TEXT
      );
      """
  conn.execute(schema);
  print("created quiz quizcontent")
  
  conn.commit()
  conn.close()
  print("new tables created and commited")

def addInitialData():
  db = db_connect()

  fin = open("startproblems.json","r")
  quiz_spec = json.load(fin)
  fin.close()

  # add page specs into the page table and linke to a quiz
  quizuid="Q34FgTYaL"
  seq=0

  for uid in quiz_spec:

      # convert the item into json format
      page_spec = quiz_spec[uid]
      page_spec_json = json.dumps(page_spec)
      print()
      print("===========================================================")
      print("uid -", uid)
      print("spec -", page_spec_json)
      print("===========================================================")
      print()
      try:

        # add page into the page table''
        db.execute( "INSERT INTO page (uid, spec) VALUES(?,?)" , (uid, page_spec_json))

        # link this page to the quiz in the quizcontent table
        db.execute( "INSERT INTO quizcontent (quizuid, pageuid, seq) VALUES(?,?,?)" , (quizuid, uid, seq,) )
        seq+=1
        
      except Exception as e:
        print(f"Error adding {uid} data : {page_spec}")
        print(f"Exception is {e}")

  # add the quiz into the quiz table
  db.execute( "INSERT INTO quiz (quizid, uid, title, details) VALUES(?,?,?,?)" , 
                     (1, quizuid, "Test quiz", "Fill in all the blanks",))
    
  
  db.commit()


  # add some users to the user database

  users = [ ("gill", "greycourt",),
            ("bob", "password123",),
            ("sally", "greycourt21",),
          ]
  

  print("adding users to users table")
  try:      
    db.executemany( 
      "INSERT INTO user (name, password) VALUES(?,?);" , 
      users)
    
    
  except Exception as e:
    print(f"Error adding users data")
    print(f"Exception is {e}")
  db.commit()  # commit after ever addition
  print("users added to users table")
  print()
  db.close()

def flask_create_database():
  # this is called from a flask route to ensure the database
  # is created in the correct location for flask to access it
  createDatabase()
  addInitialData()




# get the specs data related to the unique identifier 
# from the specs database and 
# and create the problem object that can be used
# to render the problem in html

#
# this function will 
# 1. search the page table for a record with the specified uid 
#    as a dictionary
# 2. convert the specification from json format to a dictionary
# 3. return the resulting page object
#  
# The page object is a dictionary representation of page table record i.e
#        uid      : is generated
#        title    : string containing the title for the page
#        details  : string containing the details or instructions
#        spec     : an object holding the details for this page
#
def getPage(uid):
  sql = f"SELECT * from page WHERE uid='{uid}';"
  #print(f"sql = {sql}")
  dicts = db_getdicts(sql)
  
  if not dicts:
    print(f"Error getPage() - no record in page matching uid {uid}")
    return None
  
  #db_printdicts(dicts,"matching page dicts")
  pobj = dicts[0]
  pobj["spec"] = json.loads( pobj["spec"])
  return pobj


#
# this function will 
# 1. generate a uid for this page
# 2. save the page to the page table.
#  
# The page object is a dictionary representation of page table record i.e
#   
#        title    : string containing the title for the page
#        details  : string containing the details or instructions
#        spec     : an object holding the details for this page
#
#  within this function
#       uid       : is generated
#       soec      : is converted into json format
#
#  the details can then be inserted as a new record into the page table.
#
def savePage(pobj):
  print()
  print("in savePage()")
  for key in pobj:
    print("\t", key,":",pobj[key])
  print()

  if not pobj:
    print("Error savePage() - no page object provided")
    return None;

  if not pobj.get("spec"):
    print("Error savePage() - no page specification object provided")
    return None;
  
  # generate a unique id (32char hex string)
  pobj["uid"] = db_getunique("page", "uid")

  print()
  print("converting : ", pobj["spec"])
  print()
  
  # convert the spec to json
  pobj["jspec"] = json.dumps(pobj["spec"])

  pobj["title"]   = pobj.get("title", "")
  pobj["detail"] = pobj.get("details", "")
  
  try:
    db = db_connect()
    db.execute( "INSERT INTO page (uid, title, details, spec) VALUES(?,?,?,?)" , 
                  (pobj["uid"], pobj["title"], pobj["detail"], pobj["jspec"], ))
    db.commit()  
    db.close()
    print(f'{pobj["uid"]} added successfully')
    
  except Exception as e:
    print(f"Error adding {pobj['uid']} data : {pobj['jspec']}")
    print(f"Exception is {e}")

  return pobj["uid"]



# get the uids for all the pages linked to a particular quiz uid
# return a list of the matching page uids
def getPageUids(quiz_uid):
  # search the quizcontent table for all the rows containing that quizid and get the pageid

  # search the page table for all the rows containing that pageid and get the UID
  sql = ''' SELECT qc.quizuid, p.uid AS pageuid
            FROM quizcontent AS qc, page AS p
            WHERE qc.quizuid = "{quiz_uid}"
            AND   qc.pageuid = p.uid;
        '''
  sql = sql.replace("{quiz_uid}", quiz_uid)
  
  dicts = db_getdicts(sql)
  
  # get the "pageuid" value from each dictionary and put into an array
  pageuids = [ x['pageuid'] for x in dicts] 

  return pageuids

# get the page for a specific quiz and sequence number
# return the page object
def getQuizPage(quiz_uid, quiz_seq=0):
  # search the quizcontent table for all the rows containing that quizid and get the pageid

  # get details about the quiz
  sql = f'SELECT * FROM quiz WHERE uid = "{quiz_uid}"';
  dicts = db_getdicts(sql)

  #db_printdicts(dicts, "quiz details")
  print()

  quiz = None
  if len(dicts)>0:
    quiz = dicts[0]


  # work out the maximum seq number
  sql = f'SELECT MAX(seq) FROM quizcontent WHERE quizuid = "{quiz_uid}"';
  records = db_getrecords(sql)

  #print("sql :", sql)
  #print("records :", records)

  lastseq = records[0][0]
  

  # search the page table for all the rows containing that pageid and get the UID
  sql = ''' SELECT p.*
            FROM quizcontent AS qc, page AS p
            WHERE qc.quizuid = "{quiz_uid}"
            AND   qc.pageuid = p.uid
            AND   qc.seq = {quiz_seq};
        '''
  sql = sql.replace("{quiz_uid}", quiz_uid)
  sql = sql.replace("{quiz_seq}", str(quiz_seq) )

  #print("in getQuizPage()")
  #print("sql = ", sql)  
  dicts = db_getdicts(sql)

  #db_printdicts(dicts, "page at seq position")

  page=None
  if(len(dicts)>0):  
    page = dicts[0]
  
  quizpage={}

  nav ={}
  if(quiz_seq>0):
    nav["prev"]=quiz_seq-1
  if(quiz_seq<lastseq):
    nav["next"]=quiz_seq+1
  if not nav:
    nav = None

  
  if quiz and page:
    quizpage = {  
      "quiz":quiz,
      "seq" :quiz_seq,
      "page":page,
      "nav" :nav
    }

  return  quizpage

if __name__== "__main__":
  createDatabase()
  db_tables()
  addInitialData()

  db=db_connect()
  db_print_table(db, "quiz")
  db_print_table(db, "quizcontent")
  db_print_table(db, "page")
  db_print_table(db, "user")
  db.close()

  print("==============================================")
  print("= testing getPageUids() with existing quiz uid")
  print("==============================================")
  pageuids = getPageUids("Q34FgTYaL")
  print("Q34FgTYaL :", pageuids)
  print()

  print("==============================================")
  print("= testing getPageUids() with a nonexistant quiz uid")
  print("==============================================")
  pageuids = getPageUids("THISDOESNOTEXIST")
  print("THISDOESNOTEXIST :", pageuids)
  print()

  print("==============================================")
  print("= testing db_isuniquevalue() ")
  print("= with quiz,uid, 'Q34FgTYaL' -> False ")
  print("= with quiz,uid, 'THISDOESNOTEXIST' -> True ")
  print("==============================================")
  print("Q34FgTYaL :", db_isuniquevalue("quiz", "uid", 'Q34FgTYaL') )
  print("THISDOESNOTEXIST :", db_isuniquevalue("quiz", "uid", 'THISDOESNOTEXIST') )
  print()

  
  print("==============================================")
  print("= testing db_isuniquevalue() ")
  print("= with page,uid, 'SetD' -> False ")
  print("= with page,uid, 'SetE' -> False ")
  print("= with page,uid, 'ABCdefGHI' -> True ")
  print("==============================================")
  print("setD :", db_isuniquevalue("page", "uid", 'setD') )
  print("setE :", db_isuniquevalue("page", "uid", 'setE') )
  print("ABCdefGHI :", db_isuniquevalue("page", "uid", 'ABCdefGHI') )
  print()

  print("==============================================")
  print("= testing db_getunique() ")
  print("==============================================")
  print("page and uid :", db_getunique("page", "uid") )
  print("page and uid :", db_getunique("page", "uid") )
  print("page and uid :", db_getunique("page", "uid") )
  print()
  print("quiz and uid :", db_getunique("quiz", "uid") )
  print("quiz and uid :", db_getunique("quiz", "uid") )
  print("quiz and uid :", db_getunique("quiz", "uid") )
  print()

  print("==============================================")
  print("  testing savePage() - should not produce errors ")
  print("==============================================")
  pobj1 = {
    "title"   :"test title 1",
    "details" :"test details 1",
    "spec"    :[[ 
                {"type":"text", "text":"Hello "}, 
                {"type":"fillin", "text":"world"}, 
                {"type":"text", "text":" !"} 
          ]]
  }
  print()
  print("page table - before saving page")
  db=db_connect()
  db_print_table(db, "page")
  db.close()

  print("call returns :", savePage(pobj1) )
  print()
  print("page table - after saving page")
  db=db_connect()
  db_print_table(db, "page")
  db.close()


  print()
  print("==============================================")
  print("  testing getPage() with 'setC'")
  print("      - should return validobject ")
  print("      - should not produce errors ")
  print("==============================================")
  pobj = getPage("setC")

  print("return pobj")
  print(pobj["uid"])
  print(pobj)
  print()

  print()
  print("==============================================")
  print("  testing getPage() with 'setX'")
  print("      - should return Null ")
  print("      - should produce errors ")
  print("==============================================")
  pobj = getPage("setX")

  print("return pobj")
  print(pobj)
  print()


  print()
  print("==============================================")
  print("  testing getQuizPage() with 'Q34FgTYaL'")
  print("==============================================")
  
  pobj = getQuizPage('Q34FgTYaL', 1)
  print("1.\t", pobj)
  print()

  pobj = getQuizPage('Q34FgTYaL', 2)
  print("2.\t", pobj)
  print()

  pobj = getQuizPage('Q34FgTYaL', 3)
  print("3.\t", pobj)
  print()
  
  pobj = getQuizPage('Q34FgTYaL', 4)
  print("4.\t", pobj)
  print()

  pobj = getQuizPage('Q34FgTYaL', 5)
  print("5.\t", pobj)
  print()
  
  pobj = getQuizPage('Q34FgTYaL', 0)
  print("0.\t", pobj)
  print()
  
  
  