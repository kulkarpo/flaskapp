from flask import Flask
from flask.views import MethodView
from flask import request, make_response, jsonify
import collections

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

from app import views
