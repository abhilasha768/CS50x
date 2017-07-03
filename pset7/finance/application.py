from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    # select each symbol owned by the user and it's amount
    pf_sym = db.execute("SELECT sharesno, symbol \
                                    FROM portfolio WHERE id = :id", \
                                    id=session["user_id"])
    
    # create a temporary variable to store TOTAL worth ( cash + share)
    totalcash = 0
    
    # update each symbol prices and total
    for portfolio_symbol in pf_sym:
        symbol = portfolio_symbol["symbol"]
        sharesno = portfolio_symbol["sharesno"]
        stock = lookup(symbol)
        total = sharesno * stock["price"]
        totalcash += total
        db.execute("UPDATE portfolio SET price=:price, \
                    total=:total WHERE id=:id AND symbol=:symbol", \
                    price=usd(stock["price"]), \
                    total=usd(total), id=session["user_id"], symbol=symbol)
    
    # update user's cash in portfolio
    updated_cash = db.execute("SELECT cash FROM users \
                               WHERE id=:id", id=session["user_id"])
    
    # update total cash -> cash + sharesno worth
    totalcash += updated_cash[0]["cash"]
    
    # print portfolio in index homepage
    updated_portfolio = db.execute("SELECT * from portfolio \
                                    WHERE id=:id", id=session["user_id"])
                                    
    return render_template("index.html", stocks=updated_portfolio, \
                            cash=usd(updated_cash[0]["cash"]), total= usd(totalcash) )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy sharesno of stock."""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # ensure proper symbol
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol")
        
        # ensure proper number of sharesno
        try:
            sharesno = int(request.form.get("sharesno"))
            if sharesno < 0:
                return apology("sharesno must be positive integer")
        except:
            return apology("sharesno must be positive integer")
        
        # select user's cash
        money = db.execute("SELECT cash FROM users WHERE id = :id", \
                            id=session["user_id"])
        
        # check if enough money to buy
        if not money or float(money[0]["cash"]) < stock["price"] * sharesno:
            return apology("Not enough money")
        
        # update history
        db.execute("INSERT INTO histories (symbol, sharesno, price, id) \
                    VALUES(:symbol, :sharesno, :price, :id)", \
                    symbol=stock["symbol"], sharesno=sharesno, \
                    price=usd(stock["price"]), id=session["user_id"])
                       
        # update user cash               
        db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=stock["price"] * float(sharesno))
                        
        # Select user sharesno of that symbol
        user_sharesno = db.execute("SELECT sharesno FROM portfolio \
                           WHERE id = :id AND symbol=:symbol", \
                           id=session["user_id"], symbol=stock["symbol"])
                           
        # if user doesn't has sharesno of that symbol, create new stock object
        if not user_sharesno:
            db.execute("INSERT INTO portfolio (name, sharesno, price, total, symbol, id) \
                        VALUES(:name, :sharesno, :price, :total, :symbol, :id)", \
                        name=stock["name"], sharesno=sharesno, price=usd(stock["price"]), \
                        total=usd(sharesno * stock["price"]), \
                        symbol=stock["symbol"], id=session["user_id"])
                        
        # Else increment the sharesno count
        else:
            sharesno_total = user_sharesno[0]["sharesno"] + sharesno
            db.execute("UPDATE portfolio SET sharesno=:sharesno \
                        WHERE id=:id AND symbol=:symbol", \
                        sharesno=sharesno_total, id=session["user_id"], \
                        symbol=stock["symbol"])
        
        # return to index
        return redirect(url_for("index"))
        


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    histories = db.execute("SELECT * from histories WHERE id=:id", id=session["user_id"])
    
    return render_template("history.html", histories=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        rows = lookup(request.form.get("symbol"))
        
        if not rows:
            return apology("Invalid Symbol")
            
        return render_template("quote1.html", stock=rows)
    
    else:
        return render_template("quote.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")
            
        # ensure password was submitted    
        elif not request.form.get("password"):
            return apology("Must provide password")
        
        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("passwordagain"):
            return apology("password doesn't match")
        
        # insert the new user into users, storing the hash of the user's password
        result = db.execute("INSERT INTO users (username, hash) \
                             VALUES(:username, :hash)", \
                             username=request.form.get("username"), \
                             hash=pwd_context.encrypt(request.form.get("password")))
                 
        if not result:
            return apology("Username already exist")
        
        # remember which user has logged in
        session["user_id"] = result
        # redirect user to home page
        return redirect(url_for("index"))
    
    else:
        return render_template("register.html")                


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell sharesno of stock."""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        # ensure proper symbol
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol")
        
        # ensure proper number of sharesno
        try:
            sharesno = int(request.form.get("sharesno"))
            if sharesno < 0:
                return apology("sharesno must be positive integer")
        except:
            return apology("sharesno must be positive integer")
        
        # select the symbol sharesno of that user
        user_sharesno = db.execute("SELECT sharesno FROM portfolio \
                                 WHERE id = :id AND symbol=:symbol", \
                                 id=session["user_id"], symbol=stock["symbol"])
        
        # check if enough sharesno to sell
        if not user_sharesno or int(user_sharesno[0]["sharesno"]) < sharesno:
            return apology("Not enough sharesno")
        
        # update history of a sell
        db.execute("INSERT INTO histories (symbol, sharesno, price, id) \
                    VALUES(:symbol, :sharesno, :price, :id)", \
                    symbol=stock["symbol"], sharesno=-sharesno, \
                    price=usd(stock["price"]), id=session["user_id"])
                       
        # update user cash (increase)              
        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=stock["price"] * float(sharesno))
                        
        # decrement the sharesno count
        sharesno_total = user_sharesno[0]["sharesno"] - sharesno
        
        # if after decrement is zero, delete sharesno from portfolio
        if sharesno_total == 0:
            db.execute("DELETE FROM portfolio \
                        WHERE id=:id AND symbol=:symbol", \
                        id=session["user_id"], \
                        symbol=stock["symbol"])
        # otherwise, update portfolio sharesno count
        else:
            db.execute("UPDATE portfolio SET sharesno=:sharesno \
                    WHERE id=:id AND symbol=:symbol", \
                    sharesno=sharesno_total, id=session["user_id"], \
                    symbol=stock["symbol"])
        
        # return to index
        return redirect(url_for("index"))
        
