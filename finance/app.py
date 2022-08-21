import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, , url_for
from flask_session import Session
from tempfile import mkdtemp
from time import strftime
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    rows = db.execute("SELECT symbol, name, shares FROM stocks\
                       WHERE user_id = :user_id order by symbol", \
                       user_id = session["user_id"])

    # lookup current price for each stock and culculate total value of each stock
    # add the informarion to rows to display on website
    stock_total = 0
    for row in rows:
        current_price = lookup(row["symbol"])["price"]
        total = current_price*int(row["shares"])
        row["current_price"] = usd(current_price)
        row["total"] = usd(total)
        stock_total += total

    # query table users for current cash available
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",\
            user_id = session["user_id"])[0]["cash"]

    total = cash + stock_total

    return render_template("portfolio.html", rows = rows,\
                            cash = usd(cash), total = usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # lookup a stock’s current price using
        # function "lookup" implemented in helpers.py
        quote = lookup(request.form.get("symbol"))


        # ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol")

        # ensure that stock is valid
        elif not quote:
            return apology("invalid symbol")

        # ensure amount of shares was submitted
        elif not request.form.get("shares"):
            return apology("missing shares")

        # ensure inputed number of shares is not an alphabetical string
        elif not str.isdigit(request.form.get("shares")):
            return apology("invalid shares")

         # ensure number of shares is a positive integer
        elif int(request.form.get("shares")) <= 0:
            return apology("invalid shares")

        name = quote["name"]

        # query database for username cash to check if user can afford buying shares
        rows = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"] )

        price_per_share = quote["price"]

        total_price = float(price_per_share)*int(request.form.get("shares"))

        available_cash = float(db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])[0]["cash"])

        # check if user can afford buying the shares of stock
        if available_cash < total_price:
            return apology("not enought cash! can't afford")

        else:
            # update cash in users table for the user
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = available_cash - total_price, id = session["user_id"] )

            datetime = strftime('%Y-%m-%d %H:%M:%S')

            flash("Congratulations! Transaction is successful!")

            # update user's history
            db.execute("""INSERT INTO transactions (
                          user_id, symbol, name, shares, price_per_share, total_price, transacted)
                          VALUES(:user_id, :symbol, :name, :shares, :price_per_share, :total_price, :transacted)""",\
                          user_id = session["user_id"], symbol = str.upper(request.form.get("symbol")),\
                          name = name, shares = int(request.form.get("shares")), price_per_share = price_per_share, \
                          total_price = total_price, transacted = datetime)

            # check if the stock in user's portfolio
            instock = db.execute("SELECT symbol FROM stocks WHERE user_id = :user_id and symbol = :symbol", user_id = session["user_id"], \
                                  symbol = str.upper(request.form.get("symbol")))

            if  not instock:
                # update user's portfolio (insert values)
                db.execute("""INSERT INTO stocks (
                           user_id, symbol, name, shares)
                           VALUES(:user_id, :symbol, :name, :shares)""",\
                           user_id = session["user_id"], symbol = str.upper(request.form.get("symbol")),\
                           name = name, shares = int(request.form.get("shares")))
            else:
                # update user's portfolio
                rows = db.execute("SELECT shares FROM stocks WHERE user_id = :user_id and symbol = :symbol", \
                            user_id = session["user_id"], symbol = str.upper(request.form.get("symbol")))

                db.execute("UPDATE stocks SET shares = :shares\
                            WHERE user_id = :user_id and symbol = :symbol",\
                            shares =  int(rows[0]["shares"]) + int(request.form.get("shares")),\
                            user_id = session["user_id"], symbol = str.upper(request.form.get("symbol")))


        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    name = request.args.get('username')
    names = list(db.execute("SELECT username FROM 'users' WHERE username=:username;", username=username))
    if len(username) < 1 or name in names:
        return jsonify(False)
    return jsonify(True)

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        rows = dict(lookup(request.form.get(symbol)))
        if not rows:
            return apology("Invalid symbol")

        return render_template("quoted.html", name=rows['name'], symbol=rows['symbol'], value=rows['value'])



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("The username isn't valid")
        if not password:
            return apology("The password isn't valid")
        if not confirmation:
            return apology("The password isn't valid")

        if password != confirmation:
            return apology("passwords do not match")

        password = generate_password_hash(password)
        res = db.execute("INSERT INTO users (username, password) VALUES(:username, :password);", username=name, password=password)
        if not res:
            return apology("username already exists")

    session['user_id'] = res
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
