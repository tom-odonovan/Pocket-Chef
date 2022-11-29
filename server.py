from crypt import methods
from flask import Flask, render_template, request, redirect, make_response, session
import psycopg2
from models.queries import sql_select_all, sql_select_one, sql_write
import bcrypt
import requests
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
def index():
    return render_template('login.html')


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
    session_id = session.get('user_id', 'Unknown')
    search = request.form['search']

    response = requests.get(
        f"https://api.spoonacular.com/recipes/complexSearch?query={search}&apiKey=55b5b8694b354c009c8b2c8939e1683b"
    ) 
    data = response.json()



    # result_recipes_ids = []
    # for recipe in response:
    #     result_recipes_ids.append(recipe['id'])

    # print(result_recipes_ids)

    # recipes = []

    # for id in result_recipes_ids:
    #     response = requests.get(
    #         f"https://api.spoonacular.com/recipes/{id[0]}/information?apiKey=55b5b8694b354c009c8b2c8939e1683b"
    #     )
    #     data = response.json()
    #     recipe_dict = {
    #         'id': data['id'],
    #         'title': data['title'],
    #         'image': data['image'],
    #         'prepTime': data['readyInMinutes'],
    #         'diets': data['diets']
    #     }
    #     fav_recipes.append(recipe_dict)




    if data['totalResults'] == 0:
        return render_template('no_results.html', user=session_id, search=search)
    else:
        search_results = data['results']
        # print(data)
        # print(search_results)
        return render_template('results.html', user=session_id, search=search, search_results=search_results)



@app.route('/recipe/<recipe_id>', methods=['POST', 'GET'])
def recipe(recipe_id):
    session_id = session.get('user_id', 'Unknown')
    response = requests.get(
        f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey=55b5b8694b354c009c8b2c8939e1683b"
    )
    data = response.json()

    # After much frustration I decided to create my own dictionary for each recipe as the JSON data was experiencing formatting issues

    recipe_dict = {
        'id': data['id'],
        'title': data['title'],
        'image': data['image'],
        'servings': data['servings'],
        'prepTime': data['readyInMinutes'],
        'ingredients': data['extendedIngredients'],
        'steps': data['instructions'],
        'diets': data['diets']
    }

    summary = data['summary']
    # print(summary)

    return render_template('recipe.html', user=session_id, recipe_dict=recipe_dict, summary=summary)

@app.route('/add_favourite/<recipe_id>', methods=['POST', 'GET'])
def add_favourite(recipe_id):
    session_id = session.get('user_id', 'Unknown')
    user_id = sql_select_one('SELECT id FROM users WHERE given_name=%s', [session_id])
    # print(user_id[0])
    # print(recipe_id)

    sql_write('INSERT INTO favourites (user_id, recipe_id) VALUES (%s, %s)', [user_id[0], recipe_id])

    return redirect(f'/recipe/{recipe_id}')

@app.route('/saved_recipes')
def favourite_recipes():
    session_id = session.get('user_id', 'Unknown')

    if session_id:
        user_id = sql_select_one('SELECT id FROM users WHERE given_name=%s', [session_id])
        result = sql_select_all('SELECT recipe_id FROM favourites WHERE user_id=%s', [user_id[0]])
        fav_recipes_ids = []
        for recipe in result:
            fav_recipes_ids.append(recipe)

        fav_recipes = []

        for id in fav_recipes_ids:
            response = requests.get(
                f"https://api.spoonacular.com/recipes/{id[0]}/information?apiKey=55b5b8694b354c009c8b2c8939e1683b"
            )
            data = response.json()
            recipe_dict = {
                'id': data['id'],
                'title': data['title'],
                'image': data['image'],
                'prepTime': data['readyInMinutes'],
                'diets': data['diets']
            }
            fav_recipes.append(recipe_dict)
        
        return render_template('saved_recipes.html', user=session_id, fav_recipes=fav_recipes)

    else: 
        return render_template('saved_recipes_guest.html', user=session_id)


@app.route('/delete_favourite/<recipe_id>')
def delete_favourite(recipe_id):
    session_id = session.get('user_id', 'Unknown')
    user_id = sql_select_one('SELECT id FROM users WHERE given_name=%s', [session_id])

    sql_write('DELETE FROM favourites WHERE user_id=%s AND recipe_id=%s', [user_id, recipe_id])

    return redirect('/saved_recipes')


@app.route('/user_profile')
def user_profile():
    session_id = session.get('user_id', 'Unknown')
    user_id = sql_select_one('SELECT id FROM users WHERE given_name=%s', [session_id])
    result = sql_select_all('SELECT given_name, surname, email FROM users WHERE id=%s', [user_id[0]])
    
    user_info = []
    for item in result:
        user_info.append(item)
    print(user_info)

    return render_template('user_profile.html', user=session_id, user_info=user_info)


@app.route('/planner')
def planner():
    session_id = session.get('user_id', 'Unknown')
    today = date.today()
    print(today.day)

    return render_template('planner.html', user=session_id, today=today)


@app.route('/shopping_list')
def shopping_list():
    session_id = session.get('user_id', 'Unknown')
    user_id = sql_select_one('SELECT id FROM users WHERE given_name=%s', [session_id])
    result = sql_select_all('SELECT quantity, measure, ingredient FROM shopping_list WHERE user_id=%s', [user_id[0]])
    
    shopping_list = []
    for row in result:
        quantity, measure, ingredient = row
        shopping_list.append([quantity, measure, ingredient])
    print(shopping_list)

    return render_template('shopping_list.html', user=session_id, shopping_list=shopping_list)
    
@app.route('/add_to_shopping_list')
def add_to_shopping_list():
    session_id = session.get('user_id', 'Unknown')
    
    return render_template('shopping_list.html', user=session_id)

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
