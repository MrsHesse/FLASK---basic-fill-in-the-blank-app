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



''' 
Functions for creating and managing the underlying database
'''
import sqlite3
import json

DB = "problems.db"

'''
Utility data functions
'''

def db_connect():
  try:
    db = sqlite3.connect(DB)
  except Exception as e:
    print(f"Error opening {DB} : {e}")
    db=None
  return db

  

def db_cursor(db):
    return db.cursor()


def db_tables(db=None):
  if not db:
    db=db_connect()
  if not db:
    return None
  try:
      cursor = db_cursor(db)
  except:
      print("db_tables: error creating cursor")
      return None

  try:
      sql =   """
              SELECT name FROM sqlite_master WHERE type='table';
              """
      sql =   """
              SELECT name FROM sqlite_master ;
              """

      cursor.execute(sql)
      print(cursor.fetchall())

  except:
      print("Error checking names")
      return None
  return cursor

def db_table_exists(db, tablename):
    try:
        cursor = db_cursor(db)
        sql =   "SELECT name FROM sqlite_master WHERE type='table' AND name = ?"
        cursor.execute(sql, (tablename,))
        return len(cursor.fetchall())>0

    except:
        print("Error checking names")
        return None
    return None

def db_print_table(db, tablename):

    try:
        cursor = db_cursor(db)
        sql =   "SELECT * FROM "+tablename+";"
        cursor.execute(sql)

        rows = cursor.fetchall()
        print()
        print(tablename)
        print("----------------------------")
        if len(rows)>0:
            for row in rows:
                print(row)
        else :
            print("No records in ", tablename)
            

    except Exception as e:
        print("Error printing",tablename,":", e)


def db_getrecords(select_query):
    """Returns data from an SQL query as a list of dicts."""
    records = None
    try:
        con = db_connect()
        records = con.execute(select_query).fetchall()
        
    except Exception as e:
        print(f"Failed to execute query: {select_query}\n with error:\n{e}")
        
    con.close()
    return records

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
  
  # create problem specs table
  if db_table_exists(conn, "specs"):
    conn.execute('DROP TABLE specs;')
  
  specs_schema = """
      CREATE TABLE specs(
        id INTEGER PRIMARY KEY,
        uid TEXT,
        spec text
      );
      """
  conn.execute(specs_schema);
  print("created problem-specs table")
  
  conn.commit()
  conn.close()
  print("created problem-specs table")

def addInitialData():
  db = db_connect()

  # add initial data to the specs database
  for key in Data:
      # convert the item into json format
      jsonspec = json.dumps(Data[key])

      try:
        db.execute( "INSERT INTO specs (uid, spec) VALUES(?,?)" , (key, jsonspec))
      except Exception as e:
        print(f"Error adding {key} data : {jsonspec}")
        print(f"Exception is {e}")


  # add some users to the user database

  users = [ ("gill", "greycourt",),
            ("bob", "password123",),
            ("sally", "greycourt21",),
          ]
  

  print("adding users to users table")
  try:      
    db.executemany( 
      "INSERT INTO users (name, password) VALUES(?,?);" , 
      users)
    
    
  except Exception as e:
    print(f"Error adding users data")
    print(f"Exception is {e}")
  db.commit()  # commit after ever addition
  print("users added to users table")
  print()

def flask_create_database():
  # this is called from a flask route to ensure the database
  # is created in the correct location for flask to access it
  createDatabase()
  addInitialData()




# get the specs data related to the unique identifier 
# from the specs database and 
# and create the problem object that can be used
# to render the problem in html
import uuid


# this function will be changed to get the data from
# the database when this is implemented
def getProblemObj(uid):
  # get the problem specification object format
  # for this uid

  print("in getProblemObj()")
  sql = f"SELECT spec from specs WHERE uid='{uid}'"
  print(f"sql = {sql}")
  records = db_getrecords(sql)
  print(f"records = {records}")
  
  pobj = None
  if len(records)>0:
    pobj = {} 
    pspec = json.loads(records[0][0])
    print(f"json - {records[0][0]} ")
    print(f"dict - {pspec} ")
    pobj["spec"] = pspec
  return pobj


# this function will be changed to save the data to
# the database when this is implemented
def saveProblemObj(pobj):

  # generate a unique id (32char hex string)
  uid = uuid.uuid4().hex

  Data[uid]=pobj["spec"]

  jsonspec = json.dumps(pobj["spec"])

  try:
    db = db_connect()
    db.execute( "INSERT INTO specs (uid, spec) VALUES(?,?)" , (uid, jsonspec,))
    db.commit()  
    db.close()
    print(f"{uid} added successfully")
    
  except Exception as e:
    print(f"Error adding {uid} data : {jsonspec}")
    print(f"Exception is {e}")

  return uid

def getProblemUids():
  uids=[]
  for key in Data:
    uids.append(key)
  return uids


if __name__== "__main__":
  createDatabase()
  db_tables()
  addInitialData()

  db=db_connect()
  db_print_table(db, "specs")
  db_print_table(db, "users")
  db.close()
  
