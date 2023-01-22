from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os
# from models import db
from flask_bcrypt import Bcrypt

# blueprints
import app_data
import app_image
import api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.secret_key="test"
db = SQLAlchemy()

# blueprints
app.register_blueprint(app_data.bp)
app.register_blueprint(app_image.bp)
app.register_blueprint(api.board)


db.init_app(app) # initialize app
db.app = app # imports db from models.py, asigns app to db.app
with app.app_context():
    db.create_all() # create db

if __name__ == "__main__":
    app.run(debug=True)