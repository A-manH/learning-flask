from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import sqlite3

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def create_table():
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO books (title) VALUES (?), (?), (?), (?), (?)""",
                ("To Kill a Mockingbird", "1984", "Pride and Prejudice", "The Great Gatsby", "Moby-Dick"))
    connection.commit()
    cursor.close()

def get_db_connection():
    return sqlite3.connect("books.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/catalog")
def catalog():
    connection = get_db_connection()
    cursor = connection.cursor()
    books = cursor.execute("""SELECT * FROM books""").fetchall()
    connection.close()
    return render_template("catalog.html", books=books)