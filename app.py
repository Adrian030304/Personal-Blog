from flask import Flask, request, render_template
from markupsafe import escape


app = Flask(__name__)
app.config.from_prefixed_env()



users = {}
is_admin = False


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
    return render_template('main_page.html')

@app.route('/blogs')
def blogs_page():
    return render_template('blog_page.html')


@app.route('/login',  methods=['GET','POST'])
def login_user():
    username = request.args.get('username')
    password = request.args.get('password')



    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register_user():

    username = request.args.get('username')
    password = request.args.get('password')

    if username in users:
        return 'It is already existent'

    if username and username == 'admin':
        is_admin = True

    return render_template('register.html'), 200

