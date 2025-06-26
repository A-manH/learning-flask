from os import close
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

def close_db_connection(connection):
    connection.commit()
    connection.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    if not "cart" in session:
        session["cart"] = []

    if request.method == "POST":
        try:
            book_id = request.form.get("id")
            session["cart"].append(book_id)

            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(f"""DELETE FROM books WHERE id = {book_id};""")
            close_db_connection(connection)
        except:
            print("book_id does not exist")

    connection = get_db_connection()
    cursor = connection.cursor()
    books = cursor.execute("""SELECT * FROM books""").fetchall()
    connection.close()
    return render_template("catalog.html", books=books)