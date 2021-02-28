from flask import Flask
import threading
import json
import random
import time

def run_server():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "kjahdfwi76r"
    
    from views import views

    app.register_blueprint(views, url_prefix="/")
    app.run(debug=True)


if(__name__ == "__main__"):
  run_server()