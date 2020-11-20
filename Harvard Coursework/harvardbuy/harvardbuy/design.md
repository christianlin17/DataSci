<!--A “design document” for your project in the form of a Markdown file called DESIGN.md that discusses, technically, how you implemented your project and why you made the design decisions you did. -->
<!--Your design document should be at least several paragraphs in length. Whereas your documentation is meant to be a user’s manual, consider your design document your opportunity to give the staff -->
<!--a technical tour of your project underneath its hood.-->


Introduction:
This file will be a walkthrough of our specific design choices when programming the functionalities of each html and python pages. The prose of walking through what's happening under the hood will be
intersparced with lines of code directly from our application. Each template html page will be discussed at length and lines of code will be broken down into its functional components for easy 
comprehension. Most of the functionality of the code (i.e. user input interaction with SQL) lives in application.py and the user interface of the webpage lives in their respective html template.


Layout:
Layout is our reference page in which flask helps extend styling and formatting for, especially in the design and functionality of our header and navigation bar. If you follow the comments, you can
observe the specific features of the header (i.e. Logo) and the navigation bar (i.e. drop-down menu). Besides the styling of the header and navigation bar (which is linked to our style page, 
static/style.css) a key feature in our layout is the fact that it changes the navigation bar according to whether the user is logged in or not:

        {% if session.user_id %}
          <div class="session-ongoing-buttons">
            <a value="Sell Now" href="/sell" id="sellnow-button">Sell Now</a>
            <a href="/logout">Logout</a>
          </div>
        {% else %}

If the user is logged into our website, then rather than seeing a register and a log in tab to the right of the navigation bar, they will see a Sell-Now button and a Logout button.


Register.html:
Our registration, login and logout html page is similar to the function written for Finance, and for the sake of space and brevity we will skip
these functionalities and jump straight to our key features.


Homepage.html:
Homepage first extends from the layout.html formatting, and because this webpage will borrow from bootstrap Modal popups, we had to incorporate bootstraps' 
extensions for styling source code and functions:

    {% include 'layout.html' %}

              {% extends "bootstrap/base.html" %}
              
              {% block title %}
                  Log In
              {% endblock %}
              
              {% block styles %}
              ...

The underpinnings of our homepage design is rather simple. If you observe our homepage, there are 3 rows of items on display with 6 items in each row. Those 6 numbers were
generated in the application.py (more detail in the Application.py section) according to certain features (Trending Electronics, Items under $50 etc) and we 
implemented a for loop in flask that would feed into our homepage template 6 products from our SQL database. With every box, we pulled
information such as Name, Item Description, Price, Location into a formatted product box (thank you Best Buy) and as the code iterates six
times through (from the 6 ids generated in Application.py), it produces six product box side by side of each other, and we do this 3 times.

Lastly, the part where Bootstrap comes in is when you click Buy Now, a modal popup appears that corresponds with product and item information that you're hoping to sell. The 
formatting of this modal popup came from an online template, and all the information was passed through using a separate flask for loop that changed depending on the product 
and the section of the product. To accomplish this, we created a button that would corresponded with its unique product information by assigning it a data-target that is
unique to its specific modal popup.:

   <button type="button" class="modal-btn" data-toggle="modal" data-target= "#modalQuickView-{{ item.id }}" value="Buy Now">Buy Now</button>
   
For the coding for the modal popup, we made sure that it would first iterate through all 18 ids passed on from Application.py to allow for a consistent interface, so we had three
blocks of identical code (for the modal popup) iterating through the 3 lists of products ("output", "product2", "product3"). Furthermore, each id is uniquely generated and assigned
a specific product id preventing the need for needless repetition and static inflexibility.

    {% for item in output %}
  <!-- Modal: modalQuickView https://mdbootstrap.com/docs/jquery/modals/additional/ -->
  <div class="modal fade" id="modalQuickView-{{ item.id }}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel">


  
Category.html:

Category borrows from the same concept as Homepage.html, but it's dynamic by its filter function. Rather than displaying a set amount of random products, there's a drop down menu that
you can choose to select the category of items to display. Application.py goes into more detail how it was able to reroute multiple pages of a set category to on html page, but the
category.html page pulls from Application.py all the product items that share the same category tag (using SQL SELECT) and iterates through each of them like you would see in the homepage.

      <br>
  <p class="box-announcement-cat">
      <div class="primary-cat-none">You're now browsing deals in</div><a class="primary-cat" href="/{{ category|lower }}">{{ category[0]|upper}}{{category[1:] }}</a>
  </p><br>
  <div id="rectangle"><hr/>

This allows each category page to by dynamic by the choice of menu item and has the consistent feature of modal popups to display product information in more detail. Furthermore, if you
Contact Seller, an email opens addressed to the seller with a pre-written message. This is Chris' favorite and proudest feature.



Sell.html: 
This page lets users post their items on HarvardBuy. It requires log in. 
The form asks the user for the product name, then asks the user to select where the item is located (which Harvard house/dorm), whether the seller is willing to deliver the item for free (e.g. walk to the quad...).
The seller is then asked to select which category the item should appear in, type a product description, choose a price and indicate whether it's negotiable or not. 
Finally, the seller is required to upload two pictures of the item. 




**** **** **** **** ******** **** **** **** ******** **** **** **** ****

**** **** **** **** APPLICATION.PY FILE **** **** **** **** ****

**** **** **** **** ******** **** **** **** ******** **** **** **** ****

The application.py file is the 'main engine' of our website. It process all 
the the data and is responsible for rendering all the templates. 

This section of the design file will explain how application.py works. 

Lines 1-13
Lines 1 through 13 import a number of libraries that are used at HarvardBuy,
including bootstrap, random, and a few of the libraries used in Finance. 
It also imports apology, login_required, and usd from helpers. 

Lines 15-8
Configuration code from Finance. 

Lines 42-76 (LOGIN)
The /login app route is responsible for generating the login page
and logging in the user. It also manages errors. It starts by clearing 
any existing section. If the request method is POST, meaning that data 
has been typed (we also have a javascript that checks if the textfields 
are empty in the form), we get the email and password from the form and 
query the databae to see if they exist. If we can't find the login info 
in the database, we return an error message. Otherwise we return 
homepage(). 

Lines 78-141 (HOMEPAGE)
The /homepage route is responsible for generating the homepage. 
The homepage consists of a layout component (that is generated using the 
layout.html file), and a content component (which is that is generated 
using this app route). There are three "blocks", and each contains a number 
of offers based on criteria specific in this app route section. The three
blocks are very similar, so I will only describe one of them here. The only
thing that changes is the WHERE conditions when selecting the products to
be displayed in that specific block. Let's look at the first block (or 
rectangle). The database is queried for products that meet specific 
criteria, and the ids of these products are saved in ids. Then, using 
append, I extract the ids of the products from the dictionary that I 
received from the db query. I do this because I want to randomize them 
every time the page is loaded. Using random.sample() I randomize them,
and them select products from products that have those ids. I then pass
on the product to the html page using render_template().

Lines 143-191 (SELL)
The sell app route is used to allow users to post their products to the website. 
The user inputs info about the product on the Sell Now page, and the /sell app 
route begins by getting all this data from the html page using request.form.get().
After querying the database for info (e.g. the username), a dynamic file name is
generated to avoid issues stemming from multiple pictures having the same filename.
Once everything is ready (around line 182), everything is added to the database and
the sold.html page is rendered. 

Lines 195-234 (REGISTER)
This app route allows users to register on HarvardBuy. Very similarly to Finance, it
obtains password, name, and email from the form. If the passwords don't match, an error 
is displayed. After obtaining name, email, and password, we check if the user is already 
registered using the same email. We query the database and check using a for loop if there
are any emails that match the one that has just been typed. If no matches are found, the 
password is hashed and the user is redirected to the homepage. 

Lines 237-239 (HOW)
This app route renders the how.html page which describes the main features of HarvardBuy. 


Lines ###-### (LOGOUT)
Logout logs the user out by clearing the session and by redirecting to homepage.

Lines ###-### (errorhandler(e))
From finance, handles errors, and returns apology(). 

Lines ###-### ( def category_selector(category): )
The way categories work is that there are a number of flask routes, each for a category, that look like this:

    @app.route("/lamps")
    def lamps():
      return category_selector("lamps")
    @app.route("/tables")
    def tables():
      return category_selector("tables")
    @app.route("/mirrors")
    def mirrors():
      return category_selector("mirrors")
      
When the user enters a route (e.g. by clicking the fridges category from 
the menu), that app route is called. The route for that specific category 
then calls the category_selector(category) function, which is defined 
before the category-specific app routes in the application.py file. 
Category selector takes in a category as argument, and selects all the 
elements from the database (using db.select) that belong to that category.
If the len(selection) is > 0, that means that there are indeed elements in
that category If <= zero, an error message is shown. If there are elements,
their order is randomize using random.sample, and then they are queried
from the database and rendered using the category.html template, which 
looks very similar to the homepage template. 