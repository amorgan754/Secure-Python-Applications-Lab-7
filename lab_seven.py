"""This project is to show the use of html code within python"""

#imports
from datetime import datetime
import re
import sqlite3 as sql
from flask import Flask, request, render_template, redirect


CURRENTDATE = datetime.now()


connection = sql.connect('database', check_same_thread=False)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users ([username] VARCHAR2(30), [password]
    VARCHAR2(30))''')
cur.execute('''INSERT INTO user VALUES ('admin', 'admin')''')
connection.commit()

app = Flask(__name__)


#password verification function
def passwordverification(password):
    """This function is to verify the password length"""
    if len(password) < 12:
        print("not long enough")
    elif re.search('[0-9]', password) is None:
        print("need a number")
    elif re.search('[A-Z]', password) is None:
        print("need upper number")
    elif re.search('[a-z]', password) is None:
        print("need a lower number")

#username and password verification
def userverification(username, password):
    """This function is to verify a username and password in the BD"""
    cont = False
    statement = f"SELECT username from 'users' WHERE username='{username}' AND password=\
    '{password}'"
    cur.execute(statement)
    while cont is False:
        if not cur.fetchone():
            cont = False
        else:
            cont = True
    return cont

#username and password registration
def userregistration(username, password):
    """This function is to register a username and password in the DB"""
    statement = f"INSERT INTO users VALUES ('{username}', '{password}')"
    cur.execute(statement)


#routes to pull to the different pages

#route to home page
@app.route('/')
def home():
    """This function is to pull in the home html code"""
    return render_template('home.html')

#route to current date time page, give link to world clock
@app.route('/datetime')
def date():
    """This function is to pull in the datetime html code"""
    datenow = CURRENTDATE.today()
    return render_template('datetime.html', datetime=datenow)


#route to a dad joke, give link to daily dad jokes
@app.route('/jokes')
def jokes():
    """This function is to pull in the jokes html code"""
    return render_template('jokes.html')

#route to list of books and book pages
@app.route('/books')
def books():
    """This function is to pull the books html code"""
    return render_template('books.html')

#login page route to page with the table
@app.route('/table')
def table():
    """This function is to go to the table after logging in"""
    return render_template('table.html')


#route to the user registration form
@app.route('/login', methods = ["GET", "POST"])
def login():
    """This function is to pull the login html code"""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if userverification(username, password) is True:
            return redirect('/table')
        if userverification(username, password) is False:
            return redirect('/register')
    return render_template('login.html')

#route to the user login
@app.route('/register', methods = ["GET", "POST"])
def register():
    """This function is to pull the register html code"""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        passwordverification(password)
        userregistration(username, password)
        return redirect('/table')
    return render_template('register.html')




if __name__ == '__main__':
    app.debug = True
    app.run()
