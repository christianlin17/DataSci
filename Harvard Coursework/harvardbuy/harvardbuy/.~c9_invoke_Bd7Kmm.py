import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

@app.route("/")
@login_required #user must log in to see this page
def index():
    
    id_user = session["user_id"]
    return render_template("homepage.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST": # Data has been typed in login

        email = request.form.get("email")
        password = request.form.get("password")

        # Query database for username (:something is a placeholder)
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))
                          
        
        ### NEEDS to be fixed
        namea = rows[0]["name"]
        # justname = namea.split(' ')

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("homepage.html", name=namea) #[0])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/homepage")
def homepage():
    
    return render_template("homepage.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    
    id_user = session["user_id"]
    
    if request.method == "POST": # data has been typed
        
        product_name = request.form.get("product-name")
        item_location = request.form.get("selling-locations")
        delivery_choice = request.form.get("delivery-free")
        item_description = request.form.get("item-description")
        price = request.form.get("price")
        categories = request.form.get("category")
        negotiable = request.form.get("price-negotiable")
        picture = request.form.get("picture1")
        
       #Inserting user products into the product database
        rows = db.execute("INSERT INTO products (user, name, location, delivery, price, description, category, negotiable) VALUES (:user, :product_name, :item_location, :delivery_choice, :price, :item_description, :categories, :negotiable)", user=id_user, product_name=product_name, item_location=item_location, delivery_choice=delivery_choice, price=price, item_description=item_description, categories=categories, negotiable=negotiable)
        
        return render_template("sold.html")
    
    else:
        return render_template("sell.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    
    # Forget any user_id
    session.clear()
    
    if request.method == "POST": # data has been typed

        # The password and the password confirmation have to match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 403)
    
        # Inserting user into the database 
        name = request.form.get("name")
        # hashing password 
        email = request.form.get("email")
        password_hash = generate_password_hash(request.form.get("password"))
        
        # Inserting username and password in database 
        db.execute("INSERT INTO users (email, hash, name) VALUES (:email, :h_password, :name)", email=email, name=name, h_password=password_hash)
    
        # Redirect users to homepage
        return redirect("/")
        
    # If the form is submitted using GET
    else:
        return render_template("register.html")


@app.route("/how")
def how():
    return render_template("how.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/homepage")

@app.route("/morecash", methods=["GET", "POST"])
@login_required
def morecash():
    
    if request.method == "POST":
        if not request.form.get("amount"):
            return apology("You need to insert a cash amount", 403)
        
        amount = int(request.form.get("amount"))
        if amount > 100000:
            return apology("Cannot get more than $100,000 at once", 403)
            
        if amount <= 0:
            return apology("Amount must be positive", 403)
        
        cc_raw = db.execute("SELECT cash from users where id = :user", user = session["user_id"])
        current_cash = cc_raw[0]["cash"]
        
        newcash = current_cash + amount
        
        db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash = newcash, user = session["user_id"])
        
        # Confirmation page
        return render_template("morecashconfirm.html", cash = amount)
        
    else:
        return render_template("morecash.html")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    
    # If request method is GET, show form to request a stock quote
    if request.method == "POST": # data has been typed
        if not request.form.get("symbol"): #input field name username
            return apology("You must provide a stock symbol (e.g. AAPL)", 403)
        
        output = lookup(request.form.get("symbol"))
        
        if output == None: # if the symbol doesn't exist
            return apology("Invalid stock symbol", 403)
            
        return render_template("quoted.html", symbol=output["symbol"], company=output["name"], price=output["price"])
        
    else:
        return render_template("ticker.html")





def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

