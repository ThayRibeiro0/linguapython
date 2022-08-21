
from cs50 import SQL
from flask import Flask, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///froshims.db")

REGISTRANTS = {}

SPORTS = [
    "Basketball"
    "Soccer",
    "Ultimate Frisbee",
    "Swimming",
    "Volleyball"

]

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/register", methods=["POST"])
def register():

    # Validate submission
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")

    # Remember registrant
    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", name, sport)

    # Confirm registration
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    registrants = db.execute("SELECT * FROM registrants")
    return render_template("registrants.html", registrants=registrants)


@app.route("/deregister", methods=["POST"])
def deregister():

    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect("/registrants")



# @app.route("/register", methods=["POST"])
# def register():

#     # Validate submission
#     if not request.form.get("name") or request.form.get("sport") not in SPORTS:
#         return render_template("failure.html")

#     # Confirm registration
#     return render_template("success.html")

# @app.route("/greet", methods=["POST"])
# def greet():
#     # name = request.args.post("name", "world")
#     return render_template("greet.html", name=request.form.get("name", "world"))

# @app.route("/")
# def index():
#     name = request.args.get("name")
#     return render_template("index.html", name=name)