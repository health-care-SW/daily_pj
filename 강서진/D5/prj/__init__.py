from flask import Flask, render_template
from . import app_data
from . import app_image
from . import api
from . import join

app = Flask(__name__)

app.register_blueprint(app_data.bp)
app.register_blueprint(app_image.bp)
app.register_blueprint(api.board)
app.register_blueprint(join.board)

@app.route('/')
def index():
    return render_template('index.html')