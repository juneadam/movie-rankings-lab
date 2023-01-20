"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(
        title=title, 
        overview=overview, 
        release_date=release_date, 
        poster_path=poster_path
        )

    return movie

def return_all_movies():

    return Movie.query.all()

def create_rating(user, movie, score):

    rating = Rating(user=user, movie=movie, score=score)

    return rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)