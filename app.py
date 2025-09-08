import os, json
from datetime import datetime
from random import randint
from flask import Flask, request, render_template, session, redirect, url_for
from dotenv  import *
from utils import existing_users_file, save_users, sanitize_date, sanitize_title, slugify
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_prefixed_env()
app.secret_key =  get_key('.env','FLASK_SECRET_KEY')

os.makedirs('articles', exist_ok=True)
save_path = os.path.abspath('./articles')


users_file = 'users.json'
users = existing_users_file(users_file)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET'])
def home_page():
    if 'username' not in session:
        return redirect(url_for('login_user')), 302
    return render_template('home_page.html', user=session.get('username'), user_role=session.get('role')), 200

@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect(url_for("login_user"))
    return "Welcome, Admin"


def load_articles():
    # checking if there are files in the directory
    os.makedirs(save_path, exist_ok=True)
    articles = []
    for file_name in os.listdir(save_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(save_path,file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as article_file:
                    article = json.load(article_file)
                    articles.append(article)
            except FileNotFoundError as e:
                print(f"Error: {e}")
                continue
    return sorted(articles,key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)


@app.route('/blogs')
def blogs_page():
    if 'username' not in session:
        return redirect(url_for('login_user'))
    articles = load_articles()
    return render_template('blog_page.html', user=session.get('username'), user_role='guest', articles=articles)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' not in session:
        return redirect(url_for('login_user'))
    if session.get('role') != 'admin':
        return redirect(url_for('blogs_page'))

    articles = load_articles()
    return render_template('blog_page.html', user=session.get('username'), user_role='admin', articles=articles)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_user'))

    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('blogs_page'))


@app.route('/admin/create_article', methods=['GET','POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['article_title']
        publishing = request.form['publishing_date']
        content = request.form['article_content']
        slug = f"{slugify(sanitize_title(title))}_{randint(100,999)}_{publishing}"

        save_file = os.path.join(save_path, f'{slug}.json' )
        with open(save_file, 'w', encoding='utf-8') as json_file:
            json.dump(
                {'title': title,
                 'content': content,
                 'date': sanitize_date(publishing),
                 'slug': slug
                }
            , json_file, indent=2)
        return redirect(url_for('dashboard')), 302
    return render_template('create_article.html', user=session.get('username'), user_role=session.get('role')), 200

@app.route('/article/<slug>')
def article_details(slug):
    article = os.path.join(save_path, f"{slug}.json")
    b = {}
    try:
        with open(article, 'r', encoding='utf-8') as file:
            blog = json.load(file)
            b = {
                'title': blog['title'],
                'content': blog['content'],
                'date': blog['date']
            }
    except FileNotFoundError:
        return f"Article not found", 404
    return render_template('article_details.html', 
                           user=session.get('username'), 
                           user_role=session.get('role'),
                           art=b
                           )

@app.route('/edit/<slug>', methods=['POST', 'GET'])
def article_edit(slug):
    article = os.path.join(save_path, f"{slug}.json")
    b = {}

    if request.method == 'POST':
        title = request.form['article_title']
        date = request.form['publishing_date']
        content = request.form['article_content']

        with open(article, 'w', encoding='utf-8') as json_file:
            json.dump(
                {'title': title,
                 'content': content,
                 'date': sanitize_date(date),
                 'slug': slug
                }, json_file, indent=2)

        return redirect(url_for('dashboard')), 302
    try:
        with open(article, 'r', encoding='utf-8') as file:
            blog = json.load(file)
            b = {
                'title': blog['title'],
                'content': blog['content'],
                'date': blog['date']}
    except FileNotFoundError:
        return f"Article not found", 404
    
    return render_template('edit_article.html', 
                           user=session.get('username'), 
                           user_role=session.get('role'),
                           art=b
                           )

@app.route('delete/<slug>')
def delete_article(slug):
    article = os.path.join(save_path, f"{slug}.json")
    return render_template('delete_article.html', user=session.get('username'), user_role=session.get('role'))



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

