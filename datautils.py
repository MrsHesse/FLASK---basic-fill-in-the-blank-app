import sqlite3

# global conatining the name of the current database being used
# all the utility routines access this database.
DB = None

'''
Utility data functions
'''
def db_setname(dbname):
  global DB
  DB = dbname

  # try connecting to the database to check it works
  conn = db_connect()

  if not conn:
    print(f"Error setting database to {DB}")
    return False

  return True


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

# get all the records produced by the sql query
# returns an array of tuples
def db_getrecords(select_query):
    """Returns data from an SQL query as a list of dicts."""
    records = None
    try:
        con = db_connect()
        records = con.execute(select_query).fetchall()
        
    except Exception as e:
        print(f"ERROR - db_getrecords()")
        print(f"\tfailed to execute query: {select_query}\n with error:\n{e}")
        
    con.close()
    return records

# get the first record produced by the sql query
# return a tuple
def db_getrecord(select_query):
    """Returns data from an SQL query a single tuple"""
    record = None
    try:
        con = db_connect()
        record = con.execute(select_query).fetch()
        
    except Exception as e:
        print(f"ERROR - db_getrecord()")
        print(f"\tfailed to execute query: {select_query}\n with error:\n{e}")
        
    con.close()
    return record

# get all the records produced by the sql query
# returns an array of dictionaries
# each dictionay cotains a key-value pair for each dictionary column.
def db_getdicts(select_query):
    dicts = None
    try:
        con = db_connect()
        con.row_factory = sqlite3.Row
        rows = con.execute(select_query).fetchall()
        dicts = [{k: item[k] for k in item.keys()} for item in rows]      
    except Exception as e:
        print(f"ERROR - db_getdicts()")
        print(f"\tfailed to execute query: {select_query}\n with error:\n{e}")
        
    con.close()
    return dicts

def db_printrecords(records, title=None):
  if title:
    print(title)

  if records:
    for item in records:
      print("\t", item)
  else:
    print("\t","No records produced")
  print()
  
def db_printdicts(dicts, title=None):
  if title:
    print(title)

  if dicts:
    for dict in dicts:
      print("\t", dict)
  else:
    print("\t","No dictionaries produced")
  print()
  
# used to determine if a generated id values already exists as
# a value in a particular table/column
def db_isuniquevalue(table, column, value):
  
 # search the page table for all the rows containing that pageid and get the UID
  sql = ''' SELECT {column} AS column
            FROM {table}
            WHERE {column} = "{value}";
        '''
  sql = sql.replace("{column}", column)
  sql = sql.replace("{column}", column)
  sql = sql.replace("{table}", table)
  sql = sql.replace("{value}", value)
  
  #print(sql)
  records = db_getrecords(sql)
  #db_printrecords(records, "db_isuniquevalue() result")

  return len(records)==0


import uuid

# generate a unique id for a particular table and column
def db_getunique(table, column):

  # generate a new id (32char hex string)
  newid = uuid.uuid4().hex

  while not db_isuniquevalue(table, column, newid):
    newid = uuid.uuid4().hex
  
  return newid

  

if __name__== "__main__":
  
  db_setname("problems.db")
  
  db=db_connect()
  print()
  print("page")
  db_print_table(db, "page")
  
  print()
  print("USERS")
  db_print_table(db, "users")

  print()
  print("accessing data using dictionaries")
  dicts = db_getdicts("select * from users");
  
  print("number of rows =", len(dicts))
  print()

  for r in range(len(dicts)):
    print("row :", r)
    for key in dicts[0]:
      print(f"\t{key}\t{dicts[0][key]}")
    print()

  print()
  print("accessing data using dictionaries")
  dicts = db_getdicts("select * from page");
  
  print("number of rows =", len(dicts))
  print()

  for r in range(len(dicts)):
    print("row :", r)
    for key in dicts[0]:
      print(f"\t{key}\t{dicts[0][key]}")
    print()

  db.close()



  
  
