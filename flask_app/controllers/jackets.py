from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.jacket import Jacket
from flask import flash

@app.route("/jackets/home")
def jacket_home():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(session["user_id"])
    jackets = Jacket.get_all()
    return render_template("home.html", user=user, jackets=jackets) 

@app.route('/jackets/new')
def create_jacket():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template('jacket_new.html')


@app.route('/jackets/new/process', methods=['POST'])
def process_jacket():
    if 'user_id' not in session:
        return redirect('/login')
    if not Jacket.validate_jacket(request.form):
        return redirect('/jackets/new')

    data = {
        'user_id': session['user_id'],
        'back_name': request.form['back_name'],
        'prim_color': request.form['prim_color'],
        'sec_color': request.form['prim_color'],
        'size': request.form['size'],
  
    }
    Jacket.save(data)
    return redirect('/jackets/home')



@app.route("/jackets/<int:jacket_id>")
def jacket_detail(jacket_id):
    user = User.get_by_id(session["user_id"])
    jacket = Jacket.get_by_id(jacket_id)
    return render_template("home.html", user=user, jacket=jacket)

@app.route("/jackets/create")
def show_create_page():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template("jacket_new.html")

@app.route("/jackets/edit/<int:jacket_id>")
def jacket_edit_page(jacket_id):
    jacket = Jacket.get_by_id({'id': jacket_id})
    return render_template("edit_jacket.html", jacket=jacket)


@app.route("/jackets", methods=["POST"])
def report_jacket():
    valid_jacket = Jacket.report_valid_jacket(request.form)
    if valid_jacket:
        return redirect(f'/jackets/{valid_jacket.id}')
    return redirect('/jackets/report')

@app.route("/jackets/<int:jacket_id>", methods=["POST"])
def update_jacket(jacket_id):
    if 'user_id' not in session:
        return redirect('/login')
    if not Jacket.validate_jacket(request.form):
        return redirect(f'/jackets/edit/{jacket_id}')
    valid_jacket = Jacket.update_jacket(request.form, session["user_id"])
    
    return redirect("/jackets/home")

@app.route('/jackets/view/<int:id>')
def view_jacket(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('jacket_view.html',jacket=Jacket.get_by_id({'id': id}))

@app.route("/jackets/delete/<int:jacket_id>")
def delete_by_id(jacket_id):
    Jacket.delete_jacket_by_id(jacket_id)
    return redirect("/jackets/home")

