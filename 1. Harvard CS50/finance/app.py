import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0][
        "cash"
    ]
    shares = db.execute(
        "SELECT symbol, name, quantity FROM user_stocks WHERE user_id = ?",
        session.get("user_id"),
    )
    total = cash

    for share in shares:
        share["atual_price"] = lookup(share["symbol"])["price"]
        share["total"] = share["atual_price"] * share["quantity"]
        total += share["total"]

    app.jinja_env.globals.update(usd=usd)

    return render_template(
        "index.html", shares=shares, cash=usd(cash), total=usd(total)
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("write a symbol", 400)

        elif not lookup(request.form.get("symbol")):
            return apology("invalid symbol", 400)

        elif (
            not request.form.get("shares").isnumeric()
            or float(request.form.get("shares")) < 1
        ):
            return apology("invalid shares", 400)

        stock = lookup(request.form.get("symbol"))
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))

        total = stock["price"] * float(request.form.get("shares"))

        if total > cash[0]["cash"]:
            return apology("cannot aford", 400)

        db.execute(
            "INSERT INTO stocks (user_id, name, symbol, price, shares) VALUES (?, ?, ?, ?, ?)",
            session.get("user_id"),
            stock["name"],
            stock["symbol"],
            stock["price"],
            request.form.get("shares"),
        )

        check_stock_exists = db.execute(
            "SELECT name FROM user_stocks WHERE name = ? AND user_id = ?",
            stock["name"],
            session.get("user_id"),
        )

        if not check_stock_exists:
            db.execute(
                "INSERT INTO user_stocks (user_id, name, symbol, quantity) VALUES (?, ?, ?, ?)",
                session.get("user_id"),
                stock["name"],
                stock["symbol"],
                request.form.get("shares"),
            )
        else:
            db.execute(
                "UPDATE user_stocks SET quantity = quantity + ? WHERE user_id = ? AND name = ?",
                request.form.get("shares"),
                session.get("user_id"),
                stock["name"],
            )

        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash[0]["cash"] - total,
            session.get("user_id"),
        )

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    stocks = db.execute(
        "SELECT * FROM stocks WHERE user_id = ? ORDER BY date DESC",
        session.get("user_id"),
    )

    app.jinja_env.globals.update(usd=usd)

    return render_template("history.html", stocks=stocks)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    if request.method == "POST":
        if not lookup(request.form.get("symbol")):
            return apology("invalid symbol", 400)

        stock = lookup(request.form.get("symbol"))

        return render_template("quoted.html", stock=stock, usd=usd)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        checkIfUsernameExists = db.execute(
            "SELECT username FROM users WHERE username = ?",
            request.form.get("username"),
        )

        if not request.form.get("username"):
            return apology("must provide a valid username", 400)

        elif checkIfUsernameExists:
            return apology("this username already exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Query database for username
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            generate_password_hash(
                request.form.get("password"), method="pbkdf2", salt_length=16
            ),
        )

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        sharesStock = db.execute(
            "SELECT quantity FROM user_stocks WHERE user_id = ? AND symbol = ?",
            session.get("user_id"),
            request.form.get("symbol"),
        )
        ownShares = db.execute(
            "SELECT symbol FROM user_stocks WHERE user_id = ? AND symbol = ?",
            session.get("user_id"),
            request.form.get("symbol"),
        )

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Invalid shares", 400)

        if len(ownShares) == 0 or request.form.get("symbol") != ownShares[0]["symbol"]:
            return apology("you don't have this stock", 400)

        try:
            if shares > sharesStock[0]["quantity"]:
                return apology("Invalid", 400)
            elif shares < 1:
                return apology("Invalid", 400)
        except IndexError:
            return apology("Invalid", 400)

        total = lookup(request.form.get("symbol"))["price"] * int(
            request.form.get("shares")
        )

        # User stocks
        db.execute(
            "UPDATE user_stocks SET quantity = quantity - ? WHERE user_id = ? AND symbol = ?",
            request.form.get("shares"),
            session.get("user_id"),
            request.form.get("symbol"),
        )

        # Transaction
        db.execute(
            "INSERT INTO stocks (user_id, name, symbol, price, shares) VALUES (?, ?, ?, ?, ?)",
            session.get("user_id"),
            lookup(request.form.get("symbol"))["name"],
            request.form.get("symbol"),
            lookup(request.form.get("symbol"))["price"],
            (-int(request.form.get("shares"))),
        )

        # User cash
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            total,
            session.get("user_id"),
        )

        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol, name, SUM(shares) FROM stocks WHERE user_id = ? GROUP BY name",
            session.get("user_id"),
        )
        return render_template("sell.html", stocks=stocks)
