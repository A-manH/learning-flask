from flask import Flask, render_template, request

app = Flask(__name__)

SPORTS = ["Soccer", "Basketball", "Swimming", "Golf", "Tennis",]
REGISTRANTS = {}


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    if not name:
        return render_template("error.html", error="Input name field.")

    sport = request.form.get("sport")
    if request.form.get("sport") not in SPORTS:
        return render_template("error.html", error=f'KeyError; key "{request.form.get("sport")}" is not an associated sport')
    
    REGISTRANTS[name] = sport
    print(REGISTRANTS)
    return render_template("success.html")

@app.route("/registrants")
def view_registrants():
    return render_template("registrants.html", registrants=REGISTRANTS)
