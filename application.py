import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flaskext.mysql import MySQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from controllers import user_request,quote_request, transaction

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Set up database connection
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Kien25062000#'
app.config['MYSQL_DATABASE_DB'] = 'finance'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
connectionDB = mysql.connect()
cursor = connectionDB.cursor()



# API key for searching quote information 
"""
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
    """


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = user_request.request_cash(session["user_id"], cursor=cursor)
    # get user quote info list
    quote_info = user_request.request_list_quote(session["user_id"], cursor=cursor)
    # get price from market
    quote_info = quote_request.get_quote_list_info(quote_info)
    total = cash
    for quote in quote_info:
        total = total + quote["share"] * quote["price"]
    total = round(total,2)
    return render_template('index.html',user_name = session["user_name"], quote_info = quote_info, cash = cash, total = total)


@app.route("/buy/<symbol>", methods=["GET"])
@login_required
def buy(symbol):
    """Buy shares of stock"""
    print(symbol)
    userCash = user_request.request_cash(session["user_id"], cursor)
    quote = quote_request.get_quote_info(symbol)
    maximum_share = round(userCash/quote["price"])
    return render_template("buy.html",quote = quote, cash = userCash, maximum_share = maximum_share, user_name = session["user_name"])

@app.route("/buy", methods=["POST","GET"])
@login_required
def buy_post():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        price = request.form.get("price")
        buy_share = request.form.get("buy_share")
        print(symbol)
        print(price)
        print(buy_share)
        cash = user_request.request_cash(session["user_id"], cursor = cursor)
        if float(cash) < float(price) * float(buy_share):
            return apology("Not enough cash to commit the transaction")
        else:
            transaction.commitBuy(user_id = session["user_id"], symbol = symbol, share = int(buy_share), price = float(price), cash = cash, cursor = cursor)
    return redirect("/")

#This will beused to send JSON to front end (Ajax method) - finish this later
@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return render_template("history.html")

#TO-DO: update this later
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Must include username", 403)
        elif not request.form.get("password"):
            return apology("Must include password", 403)

        username = request.form.get("username")
        password = request.form.get("password")
        searched_password = user_request.request_password(username, cursor = cursor)
        if searched_password == None or searched_password != password:
            return apology("Invalid username or password!!!", 403)
        user_id = user_request.request_user_id(username, password, cursor=cursor)
        session["user_id"] = user_id
        print(user_id)
        session["user_name"] = username
        return redirect("/")

    else:
        user_id = session.get("user_id", None)
        if user_id == None:
            return render_template("login.html")
        else:
            return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote/<chart>", methods=["GET","POST"])
@login_required
def quote(chart):
    """Get stock quote."""
    if not chart:
        return redirect("/")
    elif chart == "search":
        return render_template("quote.html",isSearch = True)
    else:
        quoteList = quote_request.get_quote_list(chart)
        return render_template("quote.html", isSearch = False, quoteList = quoteList, user_name=session["user_name"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        print("POST")
        username = request.form.get("username")
        password = request.form.get("password")
        print(username + "-" + password)

        isUsernameExist = user_request.check_username(username, cursor)
        print(isUsernameExist)
        if isUsernameExist:
            return apology("Username already exist!")
        else:
            user_request.register_user(username, password, cursor)


        return redirect("/login")

@app.route("/sell/<symbol>", methods=["GET"])
@login_required
def sell(symbol):
    """Sell shares of stock"""
    if not symbol:
        return redirect("/")
    elif request.method == "GET":
        quote = quote_request.get_quote_info(symbol)
        available_share = user_request.request_available_share(session["user_id"],symbol,cursor)
        cash = user_request.request_cash(session["user_id"],cursor)
        if quote == None:
            return redirect("/")
        elif available_share == 0:
            return apology("You have no share to sell!") #Will update this to message thing
        
        return render_template("sell.html",user_name = session["user_name"], quote = quote, available_share = available_share, cash = cash)

@app.route("/sell", methods=["GET","POST"])
@login_required
def sell_post():
    if request.method == "GET":
        return redirect("/")
    else:
        sell_share = request.form.get("sell_share")
        symbol = request.form.get("symbol")
        price = request.form.get("price")
        #To-do: do transaction here
        available_share = user_request.request_available_share(session["user_id"],symbol,cursor)
        cash = user_request.request_cash(session["user_id"], cursor)
        if int(sell_share) > available_share:
            return apology("Not enough share to sell")
        else:
            transaction.commitSell(user_id=session["user_id"],symbol=symbol,share=float(sell_share),price=float(price),cash=cash,cursor=cursor)
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
