from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__) 

connection = sqlite3.connect("shows.db")
 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("query")
    print(query)
    return redirect("/")