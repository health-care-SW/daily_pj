from flask import Flask
from . import app_data
from . import app_image

app = Flask(__name__)

app.register_blueprint(app_data.app)
app.register_blueprint(app_image.app)