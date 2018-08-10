from flask import Flask, redirect, render_template, request, session, flash
app = Flask(__name__)
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
app.secret_key="supersecret"
from mysqlconnection import connectToMySQL
mysql = connectToMySQL('aug18demo')
users = mysql.query_db('SELECT * FROM users')
print(users)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register', methods=["POST"])
def register():
    print("The form data", request.form)
    if len(request.form['username']) < 3:
        flash("Username must have at least 3 characters!")
    if len(request.form['pw']) < 3:
        flash("Passwords must have at least 3 characters!")
    if request.form['pw'] != request.form['cpw']:
        flash("Your password confirmation failed!")
    if '_flashes' in session.keys():
        return redirect("/")
    # is this username already taken?  SQL query for anyone who already has this username
    query = "SELECT * FROM users WHERE username = %(k)s;"
    data = {"k": request.form['username']}
    mysql = connectToMySQL('aug18demo')
    found = mysql.query_db(query, data)
    if found:
        flash("Username is already taken!")
        return redirect('/')
    else:
        # Create the user
        pw_hash = bcrypt.generate_password_hash(request.form['pw'])
        insertquery = "INSERT INTO users (username, pw_hash, created_at, updated_at) VALUES (%(username)s, %(pw_hash)s, NOW(), NOW());"
        insertdata = {"username": request.form['username'],
                "pw_hash": pw_hash}
        mysql = connectToMySQL('aug18demo')
        userid = mysql.query_db(insertquery, insertdata)
        session['userid'] = userid
        print("Here's what we get from found", found)
        return redirect('/wall')

@app.route('/login', methods=["POST"])
def login():
    print("Got the form data", request.form)
    # see if the username exists in the database
    query = "SELECT * FROM users WHERE username = %(username)s;"
    data = {"username" : request.form['username']}
    mysql = connectToMySQL('aug18demo')
    found = mysql.query_db(query, data)
    if found:
        # found is a list filled with one object
        # [ { 'username': 'Gonzo', pw_hash: "ajsdkfjaksdlfjkl;"} ]
        # see if the password in the database matches the one provided by the user
        if bcrypt.check_password_hash(found[0]['pw_hash'], request.form['pw']):
            session['userid'] = found[0]['id']
            return redirect('/wall')
    flash("You could not be logged in.")
    return redirect('/')

@app.route('/wall')
def wall():
    if 'userid' in session:
        return render_template('wall.html')
    else:
        flash("Please register or log in!")
        return redirect('/')

app.run(debug = True )