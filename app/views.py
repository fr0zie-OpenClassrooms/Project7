from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    """Method used to render the index template."""

    return render_template('index.html')

@app.route('/answer')
def get_answer():
    """Method used to render the answer template."""

    pass