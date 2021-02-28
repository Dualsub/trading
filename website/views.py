from flask import Blueprint, render_template, request
import json
import random
views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/portfolio-status", methods=["GET"])
def portfolio_status():
    return json.dumps({"result" : random.randint(0, 99)})