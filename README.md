# Fill in the blank puzzles
Create puzzles and deliver them to students

## Required research
- [ ] How to log in with google
  - [potential library to use](https://pythonhosted.org/Flask-GoogleLogin/)
  - [Tutorial from first principles](https://www.geeksforgeeks.org/oauth-authentication-with-flask-connect-to-google-twitter-and-facebook/)
  - [very detailed implementation](https://hackingathome.com/2020/04/25/everything-you-need-to-know-about-google-sign-in-for-web-apps/)
  - [Flask-login](https://hackingathome.com/2020/04/25/everything-you-need-to-know-about-google-sign-in-for-web-apps/)
- [ ] How to limit page access based on login credentials
- [ ] returning database records as dictionaies rather than tuples.
  - [good solution here](https://nickgeorge.net/programming/python-sqlite3-extract-to-dictionary/)
- Investigate integration with Google classroom
  - [ ] accessing rosters
  - [ ] assigning quiz to classes in classroom
  - [ ] uploading marks to google classroom


## To do

### website framework
- [x] Create flask app
- [ ] Provide login (via google)
- Separate teacher/admin area 
  - [ ] Limit access using password
  - [ ] create and manage puzzles
  - [ ] assign puzzles to classes
  - [ ] view/download/link scores
- Separate puzzle delivery area
  - [ ] use code to present quiz
  - [ ] use login details to record score in database

### Create puzzle
- [x] Page for entering/previewing/generating quiz
  - [ ] Allow spaces at start of the line
  - [ ] Allow alternative answers
  - [ ] Puzzle setting
- [x] Generated quiz allocated a unique id
- [ ] Save quiz to database 

### Create Puzzle
- [x] Page for entering/previewing/generating quiz
  - [ ] Need to include a title and instructions
- [ ] Include puzzle setting
  - [ ] case sensitive or ignore case
  - [ ] different feedback options (immediate/end/none)
- [x] Generated quiz allocated a unique id
- [ ] Save quiz to database 

### Puzzle management
- [ ] need a mechanism to view and assign puzzles to students.
- [ ] need a mechanism to deliver these puzzles to the students
- [ ] need a mechanism to record the students results when they do the puzzle.
- [ ] need a mechanism to view/save results for a class and individual students.
  - may be able to integrate with google classroom.

### Database
- [ ] Design database tables
- Create database
  - [ ] procedure to create/reset the database
  - [ ] use a route to run this procedure
- Create functions/procedures to access the database

### 








