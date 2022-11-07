from flask import Flask, render_template, request, redirect, make_response, session
import psycopg2
from models.queries import sql_select_all, sql_select_one, sql_write
import bcrypt
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/')
def index():
    return render_template('signup.html')


@app.route('/signup')
def signup():
    existing = False
    password_match = True

    return render_template('signup.html', existing=existing, password_match=password_match)


@app.route('/signup_action', methods=['POST'])
def signup_action():
    given_name = request.form.get('given_name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    admin = False

    existing_user = sql_select_one(
        'SELECT * FROM users WHERE email=%s', [email])

    if existing_user:
        existing = True
        return render_template('signup.html', existing=existing)
    if password != password_confirm:
        password_match = False
        return render_template('signup.html', password_match=password_match)
    else:
        password_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        new_user = sql_write('INSERT INTO users(email, given_name, surname, password_hash, admin) VALUES (%s, %s, %s, %s, %s)', [email, given_name, surname, password_hash, admin])

        print(f'Welcome {given_name}')
        response = redirect('/login')
        session['user_id'] = given_name
        return response



@app.route('/login')
def login():
    error = False
    return render_template('login.html', error=error)


@app.route('/login_action', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    user = sql_select_one(
        'SELECT given_name, password_hash FROM users WHERE email=%s', [username])

    if user:
        name, password_hash = list(user)
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        if valid:
            print(f'Welcome {name}')
            response = redirect('/home')
            session['user_id'] = name
            return response
        else:
            error = True
            print('Incorrect Password')
            return render_template('login.html', error=error)
    else:
        error = True
        print('User does not exist')
        return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    response = redirect('/home')
    session['user_id'] = ''
    return response


@app.route('/home')
def home():
    session_id = session.get('user_id', 'Unknown')

    return render_template('home.html', user=session_id)


@app.route('/results', methods=['POST', 'GET'])
def results():
    search = request.form['search']

    response = requests.get(
        f"https://api.spoonacular.com/recipes/complexSearch?query={search}&apiKey=65ad0a272a4d414d8a1be12d6c839a0f"
    )

    data = response.json()
    if data['totalResults'] == 0:
        return render_template('no_results.html', search=search)
    else:
        search_results = data['results']
        print(search_results)
        return render_template('results.html', search=search, search_results=search_results)


# Run the server
app.run(debug=True)
