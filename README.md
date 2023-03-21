# Pocket Chef

> Project 2 for General Assembly SEI
</br>

## Overview 

Pocket Chef is a web-based meal planner app that was created primarily as a way to oragnise your weekly meal plan and make it easy to find, share and store your favourite recipes. The goal was to take the hassle and guesswork out of cooking and create an app that has everything you need in one place. Give it a try, and let me know what you think!

## Demo 
You can access the demo version of the Pocket Chef app [here](https://meal-planner-v1.herokuapp.com/)

## Technologies
Pocket Chef was built using the following technologies:

- Python
- Flask
- postgreSQL
- Jinja2
- spoonacular API
- Postman

## Installation
To install and run Pocket Chef on your local machine, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/pocket-chef.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your own spoonacular API key by creating an account [here](https://spoonacular.com/food-api). Then, create a file named .env in the root directory of the project and add the following line:

```
SPOONACULAR_API_KEY=<your-api-key>
```

4. Create a local database instance:

```bash
python3 app.py initdb
```

5. Start the app:

```bash
python3 app.py
```

6. Open your browser and go to http://localhost:5000 to access the app.

## Features
Pocket Chef offers the following features:

- Login/Signup Functionality: Users can create an account or log in to access the app's features.
- Recipe Search: Users can search for recipes using the spoonacular API and view a list of search results.
- Detailed Recipe Information: Users can view detailed information about a recipe, including ingredients, instructions, and nutritional information.
- Adjustable Ingredient Quantities: Users can adjust the ingredient quantities based on the desired number of servings.
- Favourite Recipes: Users can save their favourite recipes to a database and view them in the favourites page.
- Meal Scheduler: Users can schedule their meals by adding recipes to their weekly calendar and view them in a dynamic weekly format.
- Shopping List: Users can add ingredients from their selected recipes to a shopping list, view it in HTML format, and check off items as they are purchased.

## Acknowledgements
Pocket Chef was developed as part of the General Assembly SEI project. Special thanks to my instructors and classmates for their support and feedback throughout the development process.

## License
Pocket Chef is licensed under the MIT License.