"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# app route to homepage
@app.route("/")
def view_homepage():
    """Load the homepage."""
# renders homepage.html template
    return render_template('homepage.html')
# app route to movies page
@app.route('/movies')
def view_movies():
    # calls function return_all_movies from crud.py and saves list of movies to
    # variable all_movies
    all_movies = crud.return_all_movies()
    # renders all_movies.html template and sends all_movies list to all_movies variable
    # on all_movies.html jinja template
    return render_template('all_movies.html', all_movies=all_movies)
# app route to movies/<movie_id> that allows movie_id variable to be passed in to url/function
@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""
    # uses movie_id variable to query movie database and get movie object, saves
    # to get_movie_by_id varible 
    get_movie_by_id = crud.get_movie_by_id(movie_id)
    # renders movie_details.html template and sends movie object (get_movie_by_id)
    # to movie variable in movie_details.html jinja template
    return render_template('movie_details.html', movie=get_movie_by_id)
#app route to /users 
@app.route('/users')
def show_all_users():
    """Display email address of each user with link to user profile"""
    # returns list of all users and saves to all_users variable by calling
    # return_all_users function in crud.py file
    all_users = crud.return_all_users()
    # renders users.html template and sends user list to all_users variable in users.html
    # jinja template
    return render_template('users.html', all_users=all_users)


# app route to /users using POST method
@app.route('/users', methods=['POST'])
def user_sign_up():
    """Check if user email already in database, if not, create a new user profile."""
    # pulls email input from sign up form on homepage.html and saves to user_email
    # variable
    user_email= request.form.get('email')
    # pulls password input from sign up form on homepage.html and saves to password
    # variable
    password = request.form.get('password')
    # passes user_email variable to get_user_by_email crud.py function to query
    # database and check for existence of user
    if crud.get_user_by_email(user_email):
        # if user exists flashes message
        flash('This user already exists. Please enter a new email.')

    else:
        # if user doesn't exist, calls create_user crud.py function and passes
        # POST request variables as arguments to create new user. Saves to new_user
        # variable
        new_user = crud.create_user(user_email, password)
        # adds new user to db
        db.session.add(new_user)
        # commits new user to db and then flashes success message
        db.session.commit()
        flash('Your account was created successfully! You may now login.')

    # redirects to homepage upon completion and flashes appropriate message
    return redirect("/")  

# app route to login using POST method
@app.route("/login", methods=['POST'])
def login_user():
    # pulls email input from form on homepage.html and saves to user_email variable
    user_email= request.form.get('email')
    # pulls password input from form on homepage.html and saves to password varialbe
    password = request.form.get('password')
    # uses post request variable as argument for get_user_by email crud.py function
    # to query user database and save user_object to variable user object
    user_object = crud.get_user_by_email(user_email)
    # saves user_object password to variable db_password
    db_password = user_object.password
    # saves user_id from user_object to variable user_id
    user_id = user_object.user_id
    # if password from input does not match password from user object
    if password != db_password:
        # flash that password is incorrect and do not store id in session
        flash("User password incorrect.")
    else:
        # stores id in session and logs user in
        session['user_id'] = user_id
        # flashes statement indicating login successful
        flash("You have logged in successfully!")
    # redirects to homepage and flashes appropriate message
    return redirect("/")
        

  #app route to users/<user_id> passes in variable user id from crud.py function      
@app.route('/users/<user_id>')
def show_user(user_id):
    """Display user profile page"""
    # saves user object to get_user_by_id by using crud.py function to query
    # user database
    get_user_by_id = crud.get_user_by_id(user_id)
    # renders user_profile.html template and passes user object (get_user_by_id) to
    # html jinja template variable user
    return render_template('user_profile.html', user=get_user_by_id)

@app.route('/user_rating', methods=['POST'])
def submit_rating():
    # get key user_rating from html input radio buttons to 
    # return html value (rating)
    rating = int(request.form.get('user_rating'))    
    rated_movie = request.form.get('movie_id')

    # if user is logged in (user_id exists in session) create new rating by
    # calling create_rating function from crud.py and passing in variables:
    # movie_object(calls get_movie_by_id function with movie_id pulled from 
    # rated_movie function)
    # user_object(calls get_user_by_id function with session user as argument)
    #adds and commits new rating to db
    if session.get('user_id'):
        movie_object = crud.get_movie_by_id(rated_movie)
        user_object = crud.get_user_by_id(session['user_id'])
        new_rating = crud.create_rating(user_object, movie_object, rating)
        db.session.add(new_rating)
        db.session.commit()
        flash(f"You have successfully given {movie_object.title} a rating of {rating}!")
        # flashes statement that tells user to login to rate a movie
    else:
        flash("You must be logged in to rate a movie.")
        
    # redirects to homepage and flashes appropriate message
    return redirect('/')
        




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
