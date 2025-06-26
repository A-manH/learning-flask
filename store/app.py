from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import sqlite3

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

def create_table():
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO books (title) VALUES (?), (?), (?), (?), (?)""",
                ("To Kill a Mockingbird", "1984", "Pride and Prejudice", "The Great Gatsby", "Moby-Dick"))
    connection.commit()
    cursor.close()

print(type(("hello",)))
