from flask import Flask , render_template
# app = Flask(__name__)  # a variable named ‘app’ which takes a string argument. It is nothing but file name, 


app = Flask("Exploring Webapp")  #If instead of “__name__” , I write file name in string format, it works perfectly fine. 
print(type(app))
print(app)

@app.route("/")    # route is a decorator. We give it a string as argument and that string is our end point. In this case URL is 
#“www.websitename.com/”. If we had written @app.route(“/blogs”) then URL would be “www.websitename.com/blogs” and whatever function
#  is written under it will be executed when anybody goes on that end point.
def hello():
    #return "Hello World !"
    return render_template("index.html")
# @app.route("/omg")
# def omg():
#     return "OM Bhanushali"
@app.route("/about")
def about():
    name='Om Gori'
    return render_template("about.html",name2=name)

@app.route("/bootstrap")
def bootstrap():
    return render_template("bootstrap.html")    
app.run(debug=True)

# Now we have written all the code for our web application but whenever we run it, nothing happens. 
# It is because we haven’t ran the application but you will say we executed the code. 
# See it like this, we make functions and run the code but functions don’t execute. Do functions execute by themselves? 
# No, we have to execute them by writing like this functionname(). 
# app.run() is like that, we are making functions but they are just there, not executed. So to execute them we need to write app.run()

# But why app.run()?
# Why app.run()? Why can’t we just write like functionname()?
#  Well we don’t want to just execute them at the same time,
#  we want a particular function to execute when user goes to that particular URL.

# Debug is an argument which we can give in app.run().
#  We don't want to restart our app everytime we make changes so it is used to automatically restart the app.

# Templates is server side and static is client side.

#Static folder:
#This folder is public, client can access it. 
# The static folder on the other hand contains the public content like the images, css, javascript and other files. 
# These files can also be viewed using the www.website-url/static address.

# Templates:
# This folder is private, client can’t access it. All the sensitive data is put in it. 
# Flask uses its template folder for storing the raw templates which can be filled through the python program.

# By default flask makes static folder public and templates folder private.
#  You can make these two folders where your python file is kept.

# render_template():
"""
Now we will do learn how to return a template(HTML page) through our python file instead just returning 'Hello World!'

First we need to make an HTML file to return so we will make that in templates folder. 
After making our webpage we have to return it through our python file. 
So for that we will go in our python file and import a function named render_template. (from flask import render_template)

from flask import Flask, render_template
Now we will use this function to render our template and return it. So for that we will write:

render_template('html_file_name.html') 
Then we start our app and open our HTML page.

Note: If we are making changes in HTML file then we don't have to reload our python app again and again as changes are made in HTML file.
 We just have to reload our page.

Like this we can make many end points(like home, about, contact) and return templates.
"""

"""
We can make a variable in our python file and send it to our HTML file. 
We can import a python module, scrap something, store that data in a variable and send it to our HTML file.
We will first make a variable and then in our render_template function pass as an argument (Refer line 20,21 in code)
To display the variable we have to use the jinja in html file  : {{Variable}}"""


"""
Tut 5:Jinja Templating 
Follow the link for notes :
https://www.codewithharry.com/videos/web-dev-using-flask-and-python-5/
"""
