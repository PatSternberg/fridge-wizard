# Fridge Hero
©2024 Bogdan Stăiculescu, Hayri Ozdemir, Kevin Eboda, Patrick Skipworth and Sam Draper

## About Fridge Hero
Fridge Hero helps you to save money and waste less food by keeping track of the expiry dates of ingredients in your fridge, alerting you when they're past their best and suggesting recipes for your next meals based on what's going off next. Become a Fridge Hero today at: URL !

### Features
- Create a user profile and keep track of items in your fridge and their expiry dates.
- Generate recipes based on the items in your fridge.

### Potential future Fridge Hero features
- Prioritise close-to-expiry items in recipes.
- Switch between multiple fridges to keep track of items across different locations or businesses.
- Automatically assign standard expiry dates for common items.
- Receive alerts when items are close to expiry.
- Access Fridge Hero from a dedicated mobile app.

### Credits
Fridge Hero was developed by Bogdan Stăiculescu, Hayri Ozdemir, Kevin Eboda, Patrick Skipworth and Sam Draper.

## Application structure
Fridge Hero uses a React framework with Javascript, a Django backend with Python and a Mongo database. Fridge Hero's frontend uses Axios to make requests to the backend, and the backend uses Pymongo to make HTTP requests to the MongoDB.

## Installing Fridge Hero
To install Fridge Hero locally:
### Clone Git repository
Go to GitHub and clone the whole Git repo.

### Install dependencies
In a terminal, `cd` to `fridge-hero/frontend/`. In the CLI, execute `npm install` to install dependencies.

In another terminal, `cd` to `fridge-hero/backend/`. In the CLI, execute `pipenv install` to install dependencies.

## Running Fridge Hero
To run Fridge Hero locally:
### Running the dev environment
You will need an active MongoDB connection to use most of Fridge Hero's features. MongoDB connections can be managed conveniently with the MongoDB Compass app. (You can download it from [here](https://www.mongodb.com/products/tools/compass))

In another terminal, `cd` to `fridge-hero/backend/`. In the CLI, execute `pipenv install` to update dependencies, then `pipenv shell` to start the virtual environment, then `python manage.py runserver` from within the virtual environment to run the backend server. By default, it runs on port 8000.

In a terminal, `cd` to `fridge-hero/frontend/`. In the CLI, execute `npm install` to update dependencies, then `npm run start` to run the frontend server. By default, it runs on port 3000. Once the `frontend` starts succesfully it should then automatically open a browser window for you with Fridge Hero. 

Alternatively, if this doesn't happen automatically; while the servers are running, open your browser of choice and navigate to http://localhost:3000/ to begin using Fridge Hero.

#### 🤩 Sign up and you'll be quickly on your way to being the hero of all of those forgotten items at the back of your fridge! 🫶🏼
#### 🎉 You know the ones we're talking about, all the things you buy on that grocery run but you *keeeep* moving further to the back... stuff that you often avoid cooking with. 
### <p align="center">💪🏼 Until now! 😉</p>


## Running tests
A suite of backend tests are included with Fridge Hero. All tests files are in `fridge-hero/backed/tests/` and use Python's unittest library to perform tests.

To run all tests, `cd` to `fridge-hero/backend`. In the CLI, execute `python -m unittest discover -v -s tests -p '*_test.py'`.

The outcome of each test will be printed in the terminal console.

### Building for production
TK
