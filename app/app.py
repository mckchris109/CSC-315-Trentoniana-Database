#! /usr/bin/python3

"""
ONE-TIME SETUP

To run this example in the CSC 315 VM you first need to make
the following one-time configuration changes:

# set the postgreSQL password for user 'lion'
sudo -u postgres psql
    ALTER USER lion PASSWORD 'lion';
    \q

# install pip for Python 3
sudo apt update
sudo apt install python3-pip

# install psycopg2
pip3 install psycopg2-binary

# install flask
pip3 install flask

# logout, then login again to inherit new shell environment
"""

"""
CSC 315
Spring 2021
John DeGood

# usage
export FLASK_APP=app.py 
flask run

# then browse to http://127.0.0.1:5000/

Purpose:
Demonstrate Flask/Python to PostgreSQL using the psycopg adapter.
Connects to the 7dbs database from "Seven Databases in Seven Days"
in the CSC 315 VM.

For psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from datetime import date
from config import config
from flask import Flask, render_template, request

#update database table using query which is an sql statement
def update(query):
    """ Connect to the PostgreSQL database server """
    #host=localhost port=5432 database=project user=lion password=lion    
    conn = psycopg2.connect(
    database ="project", user= "lion", password = "lion",host = "localhost", port = "5432"
    )
    
    conn.autocommit = True
    #attempt to run sql command
    try:
        cursor = conn.cursor()
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    conn.close()
        
def connect(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    rows = []
    try:
        # read connection parameters from database.ini
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    if rows is None:
        return 0
    return rows
 
# app.py

app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    #print(date.today())
    t = date.today() #get date
    datetemp = t.strftime('%Y-%m-%d') #format date to sql format
    #form sql statement
    temp = "INSERT INTO users (date)\nVALUES (\'" + datetemp +"\');"  
    update(temp) #call update, insert into users new user
    return render_template('my-form.html')  #load homepage

# handle form data
@app.route('/form-handler', methods=['POST'])
def handle_data():
    #print(request.form['query'])
    #print(request.form.getlist('ckname'))
    #print(request.form.getlist('ckname1'))
    #temp = "SELECT * FROM " + request.form['query'] + ";"
    searchMethod = 1; #default search method of search by jhs_name
    if len(request.form.getlist('ckname1')) == 1:
        #print("True")
        searchMethod = 2 #if selected set search method to by sound name
    if len(request.form.getlist('ckname2')) == 1:
        searchMethod = 3 #if selected set search method to view all
    #searchMethod = request.form.getlist('ckname')[0]
    #print(searchMethod)
    
    #set query to selected search method
    if searchMethod == 1 :
        temp = "SELECT * FROM information \nWHERE jhs_name = \'" + request.form['query'] + "\';";
    if searchMethod == 2 :
        temp = "SELECT * FROM information \nWHERE sound_name % \'" + request.form['query'] + "\';";
    if searchMethod == 3 :
        temp = "SELECT * FROM information;"
    #print(temp)
    rows = connect(temp) #run selected search method
    #print("Rows: ", rows)
    #rows = connect(request.form['query'])
    return render_template('my-result.html', rows=rows)  #return results page

#handle login
@app.route('/form-handler1', methods=['POST'])
def handle_data1():
   #print("HERE");
   username = request.form['loginU'] #get username
   password = request.form['loginP'] #get password
   #form sql statement
   temp = "SELECT email FROM admins \nWHERE email = \'" + username + "\' AND password = \'" + password + "\';"
   #print(username, " ", password)
   success = connect(temp) #get rows that have both the username and password
   #print(temp)
   #print(success)
   if len(success) > 0:
    #print("TRUE")
    return render_template('admin.html') #if rows exist then the admin exist so redirect to admin page
   return render_template('my-form.html') #if now rows exist then login is wrong so reload homepage

#admin update trentoniana information
@app.route('/form-handler-update', methods=['POST'])
def handle_data_update(): 
    temp = "SELECT * FROM information \nWHERE jhs_name = \'" + request.form['JName'] + "\';"
    rows = connect(temp)
    #determine if the admin entered a row that exist
    if (len(rows) == 0) or (((request.form['SoundN']) =="") and ((request.form['Link']) =="") and ((request.form['Transcript']) =="")):
        #print("FAILED")
        return render_template('admin.html') #return to admin page if no row exist
    
    '''The following if statements checks if the admin entered a value and runs
    an update on the ones entered'''
    
    temp = "UPDATE information\nSET "
    #jhs_name, sound_name, sound_link, transcript
    if not (request.form['SoundN']) =="" :
        temp = temp + " sound_name = \'" + request.form['SoundN'] + "\'\nWHERE jhs_name = \'" + request.form['JName'] + "\';"
        update(temp)
        print(temp)
        
    temp = "UPDATE information\nSET "   
    if not (request.form['Link']) =="" :
        temp = temp + " sound_link = \'" + request.form['Link'] + "\'\nWHERE jhs_name = \'" + request.form['JName'] + "\';"
        update(temp)   
        print(temp)
        
    temp = "UPDATE information\nSET "
    if not (request.form['Transcript']) =="" :
        temp = temp + " transcript = \'" + request.form['Transcript'] + "\'\nWHERE jhs_name = \'" + request.form['JName'] + "\';" 
        update(temp)  
        print(temp)
    
    #show admin what they updated, format sql statement    
    temp = "SELECT * FROM information \nWHERE jhs_name = \'" + request.form['JName'] + "\';"
    print(temp)
    rows = connect(temp)
    #print(rows)
    #return the admin page with the row of the value updated
    return render_template('admin-result.html', rows=rows)

#admin insert method 
@app.route('/form-handler-insert', methods=['POST'])
def handle_data_insert(): 
    temp = "SELECT * FROM information \nWHERE jhs_name = \'" + request.form['JName'] + "\';"
    rows = connect(temp) #check if new entry primary key already exist
    if (len(rows) > 0) or (request.form['JName']) =="":
        return render_template('admin.html')  # if it exist reload admin page
    temp = "INSERT INTO information (jhs_name)\nVALUES (\'" + (request.form['JName']) + "\');"
    #add new entry with primary key admin gave
    update(temp)
    temp = "UPDATE information\nSET "
    
    #jhs_name, sound_name, sound_link, transcript
    '''update the new entry with the data the admin provided'''
    if not (request.form['SoundN']) =="" : #check if admin entered it
        temp = temp + " sound_name = \'" + request.form['SoundN'] + "\'\nWHERE jhs_name = \'" + request.form['JName'] + "\';"  #form sql statement
        update(temp) #run sql statement
        
        
    temp = "UPDATE information\nSET "   
    if not (request.form['Link']) =="" :
        temp = temp + " sound_link = \'" + request.form['Link'] + "\'\nWHERE jhs_name = \'" + request.form['JName'] + "\';"
        update(temp)   
        
        
    temp = "UPDATE information\nSET "
    if not (request.form['Transcript']) =="" :
        temp = temp + " transcript = \'" + request.form['Transcript'] + "\'\nWHERE jhs_name = \'" + request.form['JName'] + "\';" 
        update(temp)  
        
    #show new entry the admin added
    temp = "SELECT * FROM information \nWHERE jhs_name = \'" + request.form['JName'] + "\';"
    
    rows = connect(temp)
    
    return render_template('admin-result.html', rows=rows)

#Admin delete row
@app.route('/form-handler-delete', methods=['POST'])
def handle_data_delete():
    #check if row attempting to be deleted exist
    temp = "SELECT * FROM information \nWHERE jhs_name = \'" + request.form['JName'] + "\';"
    rows = connect(temp)
    if (len(rows) == 0) or (request.form['JName']) =="":
        #if doesnt exist return to admin page
        return render_template('admin.html')
    #form sql statement and run it
    temp = "DELETE FROM information \nWHERE jhs_name = \'" + request.form['JName'] + "\';"
    update(temp)
    #show admin all entries remaining in database
    temp = "SELECT * FROM information;"
    rows = connect(temp)
    return render_template('admin-result.html', rows=rows)

#View users
@app.route('/form-handler-viewu', methods=['POST'])
def handle_data_viewu():
    temp = "SELECT * FROM users;" #view all users
    if len(request.form.getlist('ckd')) != 1:
        #if admin does not want to view all users and just wants to see a specific date
        temp = "SELECT * FROM users\nWHERE date = \'" + request.form['Date'] +"\';"
    #return admin result page populated with user info
    rows = connect(temp)
    return render_template('admin-result.html', rows=rows)

#user proposes change
@app.route('/form-propose', methods=['POST'])
def handle_data_propose():
    #if submitted blank roload page
    if (request.form['change']) =="" :
        return render_template('my-form.html')
    #if suggestion already exist reload page
    temp = "SELECT * FROM user_update\nWHERE proposed_change = \'" + (request.form['change']) + "\';"
    rows = connect(temp)
    if (len(rows) > 0):
        return render_template('my-form.html')
    #add suggestion and then send user to result page showing their suggestion
    temp = "INSERT INTO user_update (proposed_change)\nVALUES (\'" + (request.form['change']) + "\');"
    update(temp)
    temp = "SELECT * FROM user_update\nWHERE proposed_change = \'" + (request.form['change']) + "\';"
    rows = connect(temp)
    return render_template('my-result.html', rows=rows)

#admin view user updates
@app.route('/form-user-updates', methods=['POST'])
def handle_data_userupdates():
    temp = "SELECT * FROM user_update;" #default to view all
    if len(request.form.getlist('denied')) == 1:
        #set statement to denied if selected
        temp = "SELECT * FROM user_update\nWHERE status = \'Denied\';" 
    if len(request.form.getlist('verified')) == 1:
        #set statement to verified if selected
        temp = "SELECT * FROM user_update\nWHERE status = \'Verified\';"
    if len(request.form.getlist('waiting')) == 1:
        #set statement to vwaiting if selected
        temp = "SELECT * FROM user_update\nWHERE status = \'waiting\';"
    
    #search by id if value entered
    if (request.form['id']) != "":
        temp = "SELECT * FROM user_update\nWHERE update_id = \'" + request.form['id'] + "\';"
    
    #show data requested
    rows = connect(temp)
    return render_template('admin-result.html', rows=rows)

#admin update user status
@app.route('/form-user-status', methods=['POST'])
def handle_data_userstatus():
    #check if row exist, if not then reload admin page
    temp = "SELECT * FROM user_update\nWHERE update_id = \'" + request.form['id'] + "\';"
    rows = connect(temp)
    if (len(rows) == 0):
        return render_template('admin.html')
    temp = ""
    #set sql statement to value user wishes to update value to
    if len(request.form.getlist('denied')) == 1:
        temp = "UPDATE user_update\nSET status = 'Denied'\nWHERE update_id = \'" + request.form['id'] + "\';"
    if len(request.form.getlist('verified')) == 1:
        temp = "UPDATE user_update\nSET status = 'Verified'\nWHERE update_id = \'" + request.form['id'] + "\';"
    if len(request.form.getlist('waiting')) == 1:
        temp = "UPDATE user_update\nSET status = 'waiting'\nWHERE update_id = \'" + request.form['id'] + "\';"
    if temp == "" :
        return render_template('admin.html') #if no boxes selected then reload admin page
    update(temp) #update
    #return table with update value
    temp = "SELECT * FROM user_update \nWHERE update_id = \'" + request.form['id'] + "\';"
    rows = connect(temp)
    return render_template('admin-result.html', rows=rows)
    
#admin view all admins
@app.route('/form-view-admins', methods=['POST'])
def handle_data_admins(): 
    #default to select all
    temp = "SELECT * FROM admins;"
    if (request.form['email']) != "": #if value entered then search by email
        temp = "SELECT * FROM admins\nWHERE email = \'" + request.form['email'] +"\';"
    rows = connect(temp)
    return render_template('admin-result.html', rows=rows)

#admin add admin
@app.route('/form-add-admins', methods=['POST'])
def handle_add_admins():    
    if (request.form['email']) == "" or (request.form['fname']) == "" or (request.form['lname']) == "" or (request.form['password']) == "":
        return render_template('admin.html')
    temp = "SELECT * FROM admins\nWHERE email = \'" + request.form['email'] +"\';"
    rows = connect(temp)
    if len(rows) >0 :
       return render_template('admin.html')
    temp = "INSERT INTO admins (email)\nVALUES (\'" + (request.form['email']) + "\');"
    #add new entry with primary key admin gave
    update(temp)
    #add values to new row
    temp = "UPDATE admins\nSET " 
    temp = temp + " fname = \'" + request.form['fname'] + "\'\nWHERE email = \'" + request.form['email'] + "\';" 
    update(temp)  
    temp = "UPDATE admins\nSET " 
    temp = temp + " lname = \'" + request.form['lname'] + "\'\nWHERE email = \'" + request.form['email'] + "\';" 
    update(temp)  
    temp = "UPDATE admins\nSET " 
    temp = temp + " password = \'" + request.form['password'] + "\'\nWHERE email = \'" + request.form['email'] + "\';" 
    update(temp) 
    temp = "SELECT * FROM admins\nWHERE email = \'" + request.form['email'] +"\';"
    rows = connect(temp)
    #show new row
    return render_template('admin-result.html', rows=rows)

#admin delete admin
@app.route('/form-delete-admins', methods=['POST'])
def handle_delete_admins(): 
    #check if email exists
    temp = "SELECT * FROM admins\nWHERE email = \'" + request.form['email'] +"\';"
    rows = connect(temp)
    if len(rows) == 0 :
       return render_template('admin.html')  
    #delete row
    temp = "DELETE FROM admins \nWHERE email = \'" + request.form['email'] + "\';"
    update(temp)  
    #show all rows
    temp = "SELECT * FROM admins;"  
    rows = connect(temp)
    return render_template('admin-result.html', rows=rows)
    
    
#back button on results page to return user to homepage
@app.route('/back')
def vmd_timestamp():
    
    return render_template('my-form.html')

#home button on admin page to return admin to home menu
@app.route('/form-home', methods=['POST'])
def handle_home(): 
    
    return render_template('my-form.html')

#back button on admin reults page to reurnadmin to admin page
@app.route('/backA')
def back_timestamp():
    
    return render_template('admin.html')
    
if __name__ == '__main__':
    app.run(debug = True)
