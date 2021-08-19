from flask import Flask, render_template, request
from app.models import Parser, GoogleAPI, MediaWikiAPI

app = Flask(__name__)
app.config.from_object("config")


@app.route("/")
def index():
    """Method used to render the index template."""

    return render_template("index.html")


@app.route("/data", methods=["POST", "GET"])
def get_answer():
    """Method used to render the answer template."""

    question = str(request.args.get("question"))
    keywords = Parser(question)
    google_data = GoogleAPI(keywords.result)
    mediawiki_data = MediaWikiAPI(google_data.geodata)

    return render_template(
        "data.html",
        status=google_data.status,
        address=google_data.address,
        map=google_data.map,
        extract=mediawiki_data.extract,
        question=question,
    )
