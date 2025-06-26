from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import sqlite3

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def create_table():
    books_data = [
    ("To Kill a Mockingbird",),  # Each tuple represents one row
    ("1984",),
    ("Pride and Prejudice",),
    ("The Great Gatsby",),
    ("Moby-Dick",)
    ]
    
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO books (title) VALUES (?)", books_data)
    connection.commit()
    connection.close()

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
    connection = get_db_connection()
    cursor = connection.cursor()

    if not "cart" in session:
        session["cart"] = []

    if request.method == "POST":
        book_id = request.form.get("id")
        session["cart"].append(book_id)
        cursor.execute("""DELETE FROM books WHERE id = ?""", (book_id,))
    
    books_table = cursor.execute("""SELECT * FROM books""").fetchall()
    close_db_connection(connection)
    return render_template("catalog.html", books_table=books_table)

@app.route("/cart")
def view_cart():
    cart = session.get("cart")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM books WHERE id IN (?)""", cart)
    close_db_connection(connection)
    return render_template("cart.html", cart=cart)

@app.route("/reset")
def reset():
    session.clear()
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM books""")
    connection.commit()
    connection.close()
    create_table()
    return redirect("/")