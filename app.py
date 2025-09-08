import os, json
from flask import Flask, request, render_template, session, redirect, url_for, Response
from dotenv  import *
from utils import existing_users_file, save_users
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_prefixed_env()
app.secret_key =  get_key('.env','FLASK_SECRET_KEY')

users_file = 'users.json'
users = existing_users_file(users_file)

# if not os.path.exists('articles'):
#     os.mkdir('articles')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET'])
def home_page():
    if 'username' not in session:
        return redirect(url_for('login_user')), 301
    return render_template('home_page.html', user=session.get('username'), user_role=session.get('role')), 200

@app.route('/blogs')
def blogs_page():
    if 'username' not in session:
        return redirect(url_for('login_user')), 301
    
    return render_template('blog_page.html', user=session.get('username'), user_role=session.get('role'))

@app.route('/create_blog', methods=['GET','POST'])



@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect(url_for("login_user"))
    return "Welcome, Admin"

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login_user'))

@app.route('/login',  methods=['GET','POST'])
def login_user():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            return 'User does not exist!' , 403
        if username in users and (check_password_hash(users[username]['password'], password)):
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('home_page'))
        else:
            return 'Invalid name/password', 400
    
    return render_template('login.html'), 200

@app.route('/register', methods=['POST','GET'])
def register_user():

    if request.method == 'POST':
        name, pwrd = request.form['username'], request.form['password']
        if name in users:
            return 'User already exists!'
        users[name] = {'password': generate_password_hash(pwrd), 'role': 'guest'}
        if name == 'admin':
            users[name]['role'] = 'admin'
        save_users(users=users, file=users_file)

        return redirect(url_for('login_user'))
    
    return render_template('register.html'), 200

