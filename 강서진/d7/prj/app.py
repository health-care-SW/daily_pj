from flask import Flask, redirect, session
from flask_sqlalchemy import SQLAlchemy


# blueprints
import app_data
import app_image
import api
import app_post


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.secret_key="test"
db = SQLAlchemy()

# blueprints registrations
app.register_blueprint(app_data.bp)
app.register_blueprint(app_image.bp)
app.register_blueprint(api.board)
app.register_blueprint(app_post.board)

# db
db.init_app(app) # initialize app
db.app = app # imports db from models.py, asigns app to db.app
with app.app_context(): # error when omitted
    db.create_all() # create db

if __name__ == "__main__":
    app.run(debug=True)