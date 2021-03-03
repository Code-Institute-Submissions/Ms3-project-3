import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


# Configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# Register function
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # If already exists flash...
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # sign up new user in db
        mongo.db.users.insert_one({
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        })
        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Register Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


# Login function
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Profile function
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    # If username match render profile.html
    if session["user"]:
        return render_template("profile.html", username=username)
    # If not redirect to login
    return redirect(url_for("login"))


# Find notes
@app.route("/get_notes")
def get_notes():

    if session["user"]:
        # Admin has acces to all notes
        if session["user"] == "admin":
            notes = mongo.db.notes.find()
        else:
            # user sees own notes
            notes = mongo.db.notes.find({"created_by": session["user"]})

    notes = mongo.db.notes.find()
    return render_template("notes.html", notes=notes)


# Logout function
@app.route("/logout")
def logout():
    # Remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Add notes funtion
@app.route("/add_note", methods=["GET", "POST"])
def add_note():
    # Post the strings to mongo db
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        note = {
            "note_name": request.form.get("note_name"),
            "note_description": request.form.get("note_description"),
            "due_date": request.form.get("due_date"),
            "is_urgent": is_urgent,
            "created_by": session["user"]
        }
        mongo.db.notes.insert_one(note)
        flash("Note Noted!")
        return redirect(url_for("get_notes"))

    return render_template("add_notes.html")


# Edit notes function
@app.route("/edit_note/<note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    # Post the strings to mongo db
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        submit = {
            "note_name": request.form.get("note_name"),
            "note_description": request.form.get("note_description"),
            "due_date": request.form.get("due_date"),
            "is_urgent": is_urgent,
            "created_by": session["user"]
        }
        # Update the strings in mongo db
        mongo.db.notes.update({"_id": ObjectId(note_id)}, submit)
        flash("Note Updated!")

    note = mongo.db.notes.find_one({"_id": ObjectId(note_id)})
    return render_template("edit_note.html", note=note)


# Delete function
@app.route("/delete_note/<note_id>")
def delete_note(note_id):
    # Remove ObjectId from mongo db
    mongo.db.notes.remove({"_id": ObjectId(note_id)})
    flash("Note Deleted!")
    return redirect(url_for("get_notes"))


# Error Handlers
@app.errorhandler(403)
def forbidden(e):
    return render_template("error_handlers/403.html"), 403


@app.errorhandler(404)
def not_found(e):
    return render_template("error_handlers/404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error_handlers/500.html"), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
