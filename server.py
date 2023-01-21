"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def view_homepage():
    """Load the homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def view_movies():

    all_movies = crud.return_all_movies()

    return render_template('all_movies.html', all_movies=all_movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""

    get_movie_by_id = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=get_movie_by_id)

@app.route('/users')
def show_all_users():
    """Display email address of each user with link to user profile"""

    all_users = crud.return_all_users()

    return render_template('users.html', all_users=all_users)



@app.route('/users', methods=['POST'])
def user_sign_up():
    """Check if user email already in database, if not, create a new user profile."""

    user_email= request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(user_email):
        flash('This user already exists. Please enter a new email.')
        return render_template('homepage.html')
    else:
        new_user = crud.create_user(user_email, password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account was created successfully! You may now login.')
        return render_template('homepage.html')        
        


@app.route('/users/<user_id>')
def show_user(user_id):
    """Display user profile page"""

    get_user_by_id = crud.get_user_by_id(user_id)

    return render_template('user_profile.html', user=get_user_by_id)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
