from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__) 

 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = "%" + request.args.get("query") + "%"

    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    shows = cursor.execute("""
                   SELECT title FROM shows 
                        WHERE title LIKE ?
                   """, (query,)).fetchall()
    connection.commit()
    connection.close()

    return render_template("result.html", shows=shows)
