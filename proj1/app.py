from flask import Flask, render_template, request
import sqlite3

from httpx import RequestError

app = Flask(__name__)

SPORTS = ["Soccer", "Basketball", "Swimming", "Golf", "Tennis",]

def get_db_connection():
    return sqlite3.connect("sports_registration.db")

# connection = get_db_connection()
# connection = sqlite3.connect("sports_registration.db")
# # cursor = connection.cursor()
# cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS registrants(
#                 id INTEGER PRIMARY KEY,
#                name VARCHAR(20),
#                sport VARCHAR(20)
#                )
# """)

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    if not name:
        return render_template("error.html", error="Input name field.")

    sport = request.form.get("sport")
    if sport not in SPORTS:
        return render_template("error.html", error=f'KeyError; key "{request.form.get("sport")}" is not an associated sport')
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO registrants (name, sport) VALUES(?,?)""", (name, sport))
    connection.commit()
    cursor.close()
    return render_template("success.html")

@app.route("/registrants")
def view_registrants():
    connection = get_db_connection()
    cursor = connection.cursor()
    registrants = cursor.execute("""SELECT name, sport FROM registrants""").fetchall()
    cursor.close()
    return render_template("registrants.html", registrants=registrants)