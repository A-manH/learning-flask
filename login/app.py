from flask import Flask, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANEET"] = False
app.config["SESSION_TYPE"] = "filesytem"
Session(app) 