import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from flask_bootstrap import Bootstrap
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import random

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)
Bootstrap(app)

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

# counter = 0
@app.route("/")
def index():
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
        #return render_template("homepage.html", name=namea) #[0])
        return homepage()
        # https://stackoverflow.com/questions/25034123/flask-value-error-view-function-did-not-return-a-response
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/homepage")
def homepage():

    ################ FIRST RECTANGLE ################
    ids = db.execute("SELECT id FROM products WHERE price < 15000")
    # print(ids)
    
    out = []
    for ele in ids:
        out.append(ele['id']) 
    # print(out)
    
    # Source: https://stackoverflow.com/questions/46872756/extract-values-from-dictionary-to-list-in-python
    
    numbers = random.sample(out, 6)
    # print(numbers)
    
    sql_query = 'SELECT * FROM products WHERE ' + ' or '.join(('id = ' + str(n) for n in numbers))
    # Source: https://stackoverflow.com/questions/283645/python-list-in-sql-query-as-parameter
    product = db.execute(sql_query)
    
    # EUGENIO
    # username1 = 'SELECT user FROM products WHERE ' + ' or '.join(('id= ' + str(a) for a in numbers))
    # email1 = 'SELECT email FROM users WHERE ' + ' or '.join(('id= ' + str(a) for a in numbers))
    
    # userid1 = []
    # for item in userid1:
    #     userid1.append(item['username1'])
    # print(userid1)
    
    
    ################ SECOND RECTANGLE ################
    ## DO NOT DELETE COMMENTS ##
    second = db.execute("SELECT id FROM products")
    # print(second)
    
    out2 = []
    for ele in second:
        out2.append(ele['id']) 
    # print(out2)
    
    # Source: https://stackoverflow.com/questions/46872756/extract-values-from-dictionary-to-list-in-python
    
    numbers2 = random.sample(out2, 6)
    # print(numbers2)
    
    sql_query2 = 'SELECT * FROM products WHERE ' + ' or '.join(('id = ' + str(n) for n in numbers2))
    # Source: https://stackoverflow.com/questions/283645/python-list-in-sql-query-as-parameter
    product2 = db.execute(sql_query2)
    
    
    
    # Break
    list_of_users = db.execute('SELECT user FROM products WHERE ' + ' or '.join(('id = ' + str(n) for n in numbers2)))
    print(f"list of users in numbers2 is {list_of_users}")
    
    # print(len(list_of_users))
    # print(list_of_users[0]['user'])
        
    storage = []
    for i in range(len(list_of_users)):
        storage.append(list_of_users[i]['user']) 
    print(storage)
                
                
                
                
    
    ################ THIRD RECTANGLE ################
    
    ## DO NOT DELETE COMMENTS ##
    
    third = db.execute("SELECT id FROM products WHERE category = :category", category="electronics")
    # print(third)
    
    out3 = []
    for ele in third:
        out3.append(ele['id']) 
    # print(out3)
    
    # Source: https://stackoverflow.com/questions/46872756/extract-values-from-dictionary-to-list-in-python
    
    numbers3 = random.sample(out3, 6)
    # print(numbers3)
    
    sql_query3 = 'SELECT * FROM products WHERE ' + ' or '.join(('id = ' + str(n) for n in numbers3))
    # Source: https://stackoverflow.com/questions/283645/python-list-in-sql-query-as-parameter
    product3 = db.execute(sql_query3)
    

    
    ###### Sending data to homepage template 
    return render_template("homepage.html", output = product, product2 = product2, product3 = product3)

# Source: https://stackoverflow.com/questions/10125568/how-to-randomly-choose-multiple-keys-and-its-value-in-a-dictionary-python
# https://stackoverflow.com/questions/18955554/get-random-keyvalue-pairs-from-dictionary-in-python

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
        picture1 = request.files.get("picture1", "")
        picture2 = request.files.get("picture2", "")

        # filepath = "static/" + picture1.filename
        # global counter
        userinfo = db.execute("SELECT id, counter FROM users WHERE id=:user_id", user_id=session['user_id'])[0]
        counter=userinfo['counter']
        username=userinfo['id']
        counter += 1
        extension = picture1.filename.split('.')[-1]
        filepath = "static/" + str(username) + "-" + str(counter) + '.' + extension
        counter += 1
        # filepath2 = "static/" + picture2.filename
        extension = picture2.filename.split('.')[-1]
        filepath2 = "static/" + str(username) + "-" + str(counter) + '.' + extension
        db.execute("UPDATE users SET counter = :counter WHERE id=:user_id", counter=counter, user_id=session['user_id'])

        if filepath is not None:
            with open(filepath, 'wb') as f:
                f.write(picture1.read())
                
        if filepath2 is not None:
            with open(filepath2, 'wb') as f:
                f.write(picture2.read())

       #Inserting user products into the product database
        rows = db.execute("INSERT INTO products (user, name, location, delivery, price, description, category, negotiable, picture1, picture2) VALUES (:user, :product_name, :item_location, :delivery_choice, :price, :item_description, :categories, :negotiable, :picture1, :picture2)", user=id_user, product_name=product_name, item_location=item_location, delivery_choice=delivery_choice, price=price, item_description=item_description, categories=categories, negotiable=negotiable, picture1=filepath, picture2=filepath2)
        # image = db.execute("SELECT picture1 FROM products")
        # for i in image:
        #     print(i['picture1'])
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
        
        # Check if user already exists
        list_users = db.execute("SELECT email FROM users")
        print(list_users)
        
        print(len(list_users))
        print(list_users[0]['email'])
        
        for i in range(len(list_users)):
            if list_users[i]['email'] == email:
                return apology("Email already exists", 403)
        
        # Get password from form
        password_hash = generate_password_hash(request.form.get("password"))

        # Inserting username and password in database
        db.execute("INSERT INTO users (email, hash, name) VALUES (:email, :h_password, :name)", email=email, name=name, h_password=password_hash)

        # Redirect users to homepage
        return redirect("/login")

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

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# Category page generation using category.html template
def category_selector(category):
    
    # print(category)
    elements = db.execute("SELECT id FROM products WHERE category = :category", category = category)
    # print(elements)
    
    selection = []
    for ele in elements:
        selection.append(ele['id']) 
        
    # print(f"length is {len(selection)}")
    
    if len(selection) > 0:
    
        # Source: https://stackoverflow.com/questions/46872756/extract-values-from-dictionary-to-list-in-python
        numbers3 = random.sample(selection, len(selection))
        # print(numbers3)
        
        sql_query3 = 'SELECT * FROM products WHERE ' + ' or '.join(('id = ' + str(n) for n in numbers3))
        # Source: https://stackoverflow.com/questions/283645/python-list-in-sql-query-as-parameter
        category_selected = db.execute(sql_query3)
        
        ###### Sending data to homepage template 
        return render_template("category.html", category = category.title(), output = category_selected)

    else:
        return apology("Empty category", 403)
        
        
# Categories 
@app.route("/futons")
def futons():
    return category_selector("futons")
    
@app.route("/fridges")
def fridges():
    return category_selector("fridges")
    
@app.route("/chairs")
def chairs():
    return category_selector("chairs")

@app.route("/lamps")
def lamps():
    return category_selector("lamps")
    
@app.route("/tables")
def tables():
    return category_selector("tables")
    
@app.route("/mirrors")
def mirrors():
    return category_selector("mirrors")
    
@app.route("/rugs")
def rugs():
    return category_selector("rugs")
    
@app.route("/other-furniture")
def other_furniture():
    return category_selector("other-furniture")
    
@app.route("/men")
def men():
    return category_selector("men")
    
@app.route("/women")
def women():
    return category_selector("women")
    
@app.route("/other-clothes")
def other_clothes():
    return category_selector("other-clothes")
    
@app.route("/books")
def books():
    return category_selector("books")
    
@app.route("/fans")
def fans():
    return category_selector("fans")
    
@app.route("/electronics")
def electronics():
    return category_selector("electronics")
    
@app.route("/other-misc")
def other_misc():
    return category_selector("other-misc")
    