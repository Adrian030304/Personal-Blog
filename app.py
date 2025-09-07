import os, json
from flask import Flask, request, render_template, session, redirect, url_for, Response
from dotenv  import *
from utils import check_auth, authenticate

app = Flask(__name__)
app.config.from_prefixed_env()

secret_key = get_key('.env','FLASK_SECRET_KEY')

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

    # checking if header exists
    auth_header = request.headers.get('Authorization')
    if not check_auth(auth_header, username, password)
        return authenticate()
    if request.method == 'POST':
        pass
    return render_template('register.html'), 200

