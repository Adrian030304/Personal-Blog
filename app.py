import os, json
from flask import Flask, request, render_template, session, redirect, url_for, Response
from dotenv  import *
from utils import existing_users_file, save_users

app = Flask(__name__)
app.config.from_prefixed_env()

secret_key = get_key('.env','FLASK_SECRET_KEY')

users_file = 'users.json'
users = existing_users_file()
save_users(users=users, file=users_file)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
    return render_template('main_page.html')

@app.route('/blogs')
def blogs_page():
    return render_template('blog_page.html')


@app.route('/login',  methods=['GET','POST'])
def login_user():
    # username = request.form['username']
    # password = request.form['password']

    
    # if username not in session:
    #     session['username'] = username
    #     session['password'] = generate_password_hash(password)
    #     session['is_admin'] = False
    return render_template('login.html'), 200

@app.route('/register', methods=['POST','GET'])
def register_user():
    if request.method == 'POST':

    return render_template('register.html'), 200

