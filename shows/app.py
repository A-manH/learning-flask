from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__) 

 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = "%" + request.args.get("query") + "%"

    connection = sqlite3.connect("show.db")
    cursor = connection.cursor()
    query_results = cursor.execute("""
                   SELECT title FROM shows 
                        WHERE title LIKE ?
                   """, (query,)).fetchall()
    connection.commit()
    connection.close()
    print(query_results)

    return render_template("results.html", results=query_results)