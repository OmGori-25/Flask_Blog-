from flask import Flask , render_template , request, session, redirect
from flask_mail import Mail
import json
import math
import os
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from werkzeug.utils import secure_filename


with open("config.json",'r') as c :
    params=json.load(c)['params']

local_server = params['local_server']
app=Flask(__name__)
app.secret_key='super secret key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = '465',
    MAIL_USE_SSL=True ,
    MAIL_USERNAME=params["mail_user"],
    MAIL_PASSWORD=params["mail_password"]
)
mail=Mail(app)

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"]=params["local_uri"]
else :
    app.config["SQLALCHEMY_DATABASE_URI"]=params["prod_uri"]    
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/codingthunder'

db=SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email_id = db.Column(db.String(20), nullable=False)
    contact_no = db.Column(db.String(15), nullable=False)
    msg = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Posts(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    subtitle=db.Column(db.String(100), nullable=False)
    slug=db.Column(db.String(25), nullable=False)
    content=db.Column(db.String(500), nullable=False)
    img_file=db.Column(db.String(20), nullable=False)
    date=db.Column(db.String(20), nullable=True)

@app.route("/")
def home():
    posts=Posts.query.filter_by().all()
    last=math.ceil(len(posts)/params["no_of_posts"])

    page=request.args.get('page')
    if not str(page).isnumeric():
        page=1
    page=int(page)
    posts=posts[(page-1)*params["no_of_posts"]:(page-1)*params["no_of_posts"]+params["no_of_posts"]]
    if page==1:
        prev="#"
        next="/?page="+ str(page+1)
        
    elif page==last :
        prev="/?page=" + str(page-1)
        next="#"
    else :
        prev="/?page=" + str(page-1)
        next="/?page="+ str(page+1)

   
    return render_template("index.html",params=params,posts=posts,prev=prev, next=next)

@app.route("/delete/<string:sno>",methods=["GET","POST"])
def delete(sno):
    if 'user' in session and session['user']==params["admin_user"]:
       posts=Posts.query.filter_by(sno=sno).first()
       db.session.delete(posts)
       db.session.commit()
       return redirect("/dashboard")



@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")

@app.route("/uploader", methods=['GET','POST'])
def uploader():
    if 'user' in session and session['user']==params["admin_user"]:
        if request.method=="POST":
            f=request.files['file1'] 
            f.save(os.path.join(app.config["UPLOAD_FOLDER"]), secure_filename(f.filename))
            return "Uploaded Successfully"
        
@app.route("/edit/<string:sno>",methods=["GET","POST"])
def edit(sno):
    if 'user' in session and session['user']==params["admin_user"]:
        if request.method=='POST':
            box_title=request.form.get("title")
            tline=request.form.get("tline")
            slug=request.form.get("slug")
            content=request.form.get("content")
            img_file=request.form.get("img_file")

            if sno=="0":
                post=Posts(title=box_title,subtitle=tline,slug=slug,content=content,img_file=img_file,date=datetime.now())
                db.session.add(post)
                db.session.commit()
        
            else:
                post=Posts.query.filter_by(sno=sno).first()
                post.title=box_title
                post.subtitle=tline
                post.slug=slug 
                post.content=content
                post.img_file=img_file
                db.session.commit()
                return redirect("/edit/"+sno)
        post=Posts.query.filter_by(sno=sno).first()
        return render_template("edit.html",params=params,post=post,sno=sno) 


@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if 'user' in session and session['user']==params['admin_user']:
        posts=Posts.query.all()
        return render_template("dashboard.html",params=params,posts=posts)
    
    if request.method=='POST':
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if (username==params["admin_user"] and (userpass==params["admin_pass"])):
            #Set the session variable
            session['user']=username
            posts=Posts.query.all()
            return render_template("dashboard.html",params=params,posts=posts)

    
    return render_template("login.html",params=params)

@app.route("/about")
def about():
    return render_template("about.html",params=params)

@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html",params=params, post=post)

@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        # Fetch data and add it to the database
        name=request.form.get('name')
        email=request.form.get('email')
        phone_no=request.form.get('phone_no')
        message=request.form.get('message')
        entry=Contacts(name=name, email_id=email, contact_no=phone_no, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit() 
        mail.send_message('New message from' + name,
                          sender=email,
                          recipients=[params['mail_user']],
                          body=message + "\n" + phone_no + email
                           
                          )
    return render_template("contact.html",params=params)

app.run(debug=True)