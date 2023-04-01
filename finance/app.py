import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    # Query database for id
    user_id = session["user_id"]
    rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    # Obtain user info
    username = rows[0]["username"]
    cash = rows[0]["cash"]

    # Query for all puchases by user
    dictHoldings = db.execute("SELECT stock, shares FROM holdings WHERE user_id = ?", user_id)

    # Obtain total equity
    total_equity = 0

    for dictHolding in dictHoldings:
        dictSymbol = lookup(dictHolding["stock"])
        price = dictSymbol["price"]
        dictHolding["price"] = price
        total_value = round(dictHolding["shares"] * price, 5)
        dictHolding["total_value"] = total_value

        # Obtain total quity
        total_equity += total_value

    # Obtain cash and total assets
    total_assets = cash + total_equity
    cash = round(cash, 2)
    total_assets = round(total_assets, 5)

    return render_template("homepage.html", username=username, cash=cash, total_equity=total_equity, total_assets=total_assets, dictHoldings=dictHoldings)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        user_id = session["user_id"]

        # Ensure stock is valid
        symbol = request.form.get("symbol").upper()
        dictSymbol = lookup(symbol)
        if not dictSymbol:
            return apology("must provide valid stock", 403)

        # Ensure shares > 0
        shares = request.form.get("shares")
        if not shares or float(shares) <= 0:
            return apology("must buy at least 1 share", 403)
        else:
            shares = float(shares)


        # Look up Company Name and Stock Price
        name = dictSymbol["name"]
        price = dictSymbol["price"]

        # Query database for id
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Obtain user info
        username = rows[0]["username"]
        cash = rows[0]["cash"]

        # Obtain current datetime
        now = datetime.now()
        current_date = date.today()
        current_time = now.strftime("%H:%M:%S")

        # Reject purchase if insufficient funds for purchase
        purchase_cost = shares * price
        if cash < purchase_cost:
            return apology("insufficient funds for purchase", 403)


        # Deduct funds from user TABLE
        remaining_funds = cash - purchase_cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining_funds, user_id)

        # Update transactions TABLE
        db.execute("INSERT INTO transactions (user_id, username, stock, action, price, shares, total_value, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, username, symbol, 'Buy', price, shares, purchase_cost, current_date, current_time)

        rowHoldings = db.execute("SELECT * FROM holdings WHERE user_id = ? AND stock = ?", user_id, symbol)

        if len(rowHoldings) == 1:
            db.execute("UPDATE holdings SET shares = shares + ? WHERE user_id = ? AND stock = ?", shares, user_id, symbol)
        else:
            db.execute("INSERT into holdings (user_id, username, stock, shares) VALUES (?, ?, ?, ?)", user_id, username, symbol, shares)

        # Redirect user to home page
        return render_template("success.html", action="Transaction", message=f"{shares} shares of {symbol} bought")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    rowsHistory = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC, time DESC", user_id)

    return render_template("history.html", rowsHistory=rowsHistory)


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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Remember symbol
        symbol = request.form.get("symbol").upper()
        dictSymbol = lookup(symbol)

        # Check if stock exists
        if dictSymbol:
            name = dictSymbol["name"]
            price = f"${dictSymbol['price']}"
        else:
            symbol = f"'{symbol}' not found"
            name = "-"
            price = "-"

        return render_template("quote.html", symbol=symbol, name=name, price=price)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        password = request.form.get("password")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure username is unique
        elif len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) == 1:
            return apology("username has been taken", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Ensure password confirmation was submitted
        elif password != request.form.get("confirmation"):
            return apology("must provide valid password confirmation", 403)

        # Ensure password is validated
        else:
            upper = 0
            lower = 0
            number = 0
            for char in password:
                if char.isupper():
                    upper += 1
                if char.islower():
                    lower += 1
                if char.isnumeric():
                    number += 1
            if upper == 0 or lower == 0 or number == 0 or len(password) < 8:
                return apology("must provide valid password", 403)

        # Remember user
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        user_id = session["user_id"]

        # Ensure stock is valid
        symbol = request.form.get("symbol").upper()
        dictSymbol = lookup(symbol)
        if not dictSymbol:
            return apology("must provide valid stock", 403)

        # Ensure shares > 0
        shares = request.form.get("shares")
        if not shares or float(shares) <= 0:
            return apology("must sell at least 1 share", 403)
        else:
            shares = float(shares)


        # Look up Company Name and Stock Price
        name = dictSymbol["name"]
        price = dictSymbol["price"]

        # Query database for id
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        rowHoldings = db.execute("SELECT * FROM holdings WHERE user_id = ? and stock = ?", user_id, symbol)
        if len(rowHoldings) != 1:
            return apology("you do not hold this stock", 403)

        # Reject purchase if insufficient shares for sale
        shares_holding = rowHoldings[0]["shares"]
        if shares > shares_holding:
            return apology("insufficient shares for sale", 403)

        # Obtain user info
        username = rows[0]["username"]
        cash = rows[0]["cash"]

        # Obtain current datetime
        now = datetime.now()
        current_date = date.today()
        current_time = now.strftime("%H:%M:%S")

        # Deduct funds from user TABLE
        sales_revenue = shares * price
        remaining_funds = cash + sales_revenue
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining_funds, user_id)

        # Update transactions TABLE
        db.execute("INSERT INTO transactions (user_id, username, stock, action, price, shares, total_value, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, username, symbol, 'Sell', price, shares, sales_revenue, current_date, current_time)

        # Update holdings TABLE
        rowHoldings = db.execute("SELECT * FROM holdings WHERE user_id = ? AND stock = ?", user_id, symbol)
        if len(rowHoldings) == 1:
            db.execute("UPDATE holdings SET shares = shares - ? WHERE user_id = ? AND stock = ?", shares, user_id, symbol)
        else:
            db.execute("INSERT into holdings (user_id, username, stock, shares) VALUES (?, ?, ?, ?)", user_id, username, symbol, shares)

        # Redirect user to home page
        return render_template("success.html", action="Transaction", message=f"{shares} shares of {symbol} sold")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if request.form['settings_button'] == 'change password':
            return redirect("/change_password")
        elif request.form['settings_button'] == 'deposit funds':
            return redirect("/deposit_funds")
        elif request.form['settings_button'] == 'withdraw funds':
            return redirect("/withdraw_funds")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("settings.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user_id = session["user_id"]
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        new_password_confirmation = request.form.get("new_password_confirmation")

        # Query database for user_id
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure username exists and password is correct
        if not check_password_hash(rows[0]["hash"], old_password):
            return apology("invalid password", 403)

        # Ensure password confirmation was submitted
        elif new_password != request.form.get("new_password_confirmation"):
            return apology("must provide valid password confirmation", 403)

        # Ensure password is validated
        else:
            upper = 0
            lower = 0
            number = 0
            for char in new_password:
                if char.isupper():
                    upper += 1
                if char.islower():
                    lower += 1
                if char.isnumeric():
                    number += 1
            if upper == 0 or lower == 0 or number == 0 or len(new_password) < 8:
                return apology("must provide valid new password", 403)

        # Remember user
        hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)
        return render_template("success.html", action="Change", message="Password change completed")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")

@app.route("/deposit_funds", methods=["GET", "POST"])
@login_required
def deposit_funds():

    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        funds = float(request.form.get("funds"))
        if funds < 0.01:
            return apology("must deposit valid funds", 403)

        # Query database for id
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        username = rows[0]["username"]
        cash = rows[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash+funds, user_id)

        # Obtain current datetime
        now = datetime.now()
        current_date = date.today()
        current_time = now.strftime("%H:%M:%S")

        # Update Transactions TABLE
        db.execute("INSERT INTO transactions (user_id, username, action, total_value, date, time) VALUES (?, ?, ?, ?, ?, ?)", user_id, username, 'Deposit', funds, current_date, current_time)

        return render_template("success.html", action="Transaction", message=f"${funds} deposited")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("deposit_funds.html")

@app.route("/withdraw_funds", methods=["GET", "POST"])
@login_required
def withdraw_funds():

    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        funds = float(request.form.get("funds"))
        if funds < 0.01:
            return apology("must withdraw valid funds", 403)

        # Query database for id
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        username = rows[0]["username"]
        cash = rows[0]["cash"]
        if cash < funds:
            return apology("insufficient funds for withdrawal", 403)

        # Obtain current datetime
        now = datetime.now()
        current_date = date.today()
        current_time = now.strftime("%H:%M:%S")

        # Update Transactions TABLE
        db.execute("INSERT INTO transactions (user_id, username, action, total_value, date, time) VALUES (?, ?, ?, ?, ?, ?)", user_id, username, 'Withdrawal', funds, current_date, current_time)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash-funds, user_id)
        return render_template("success.html", action="Transaction", message=f"${funds} withdrawn")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("withdraw_funds.html")

@app.route("/success", methods=["POST"])
@login_required
def success():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        return redirect("/")