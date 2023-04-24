from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/register/process", methods=["POST"])
def register():
    if not User.valid_user(User,request.form):
        return redirect("/")
    data ={ 
        "email": request.form['email'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    valid_user = User.save(data)
    session["user_id"] = valid_user
    flash("Thank you for registering","register")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    valid_user = User.authenticated_user_by_input(request.form)
    if not valid_user:
        flash("Invalid Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(valid_user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session["user_id"] = valid_user.id
    return redirect('/jackets/home')




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
