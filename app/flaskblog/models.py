from flaskblog import db
from flaskblog import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Admin(db.Model):
	username = db.Column("Admin11")
	password = db.Column("muskan")


class AddPlaces(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cityName = db.Column(db.String(100), unique=True, nullable=False)
	placeName = db.Column(db.String(100), unique=True, nullable=False)
	image = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(100), unique=True, nullable=False)
	features = db.Column(db.String(100), unique=True, nullable=False)