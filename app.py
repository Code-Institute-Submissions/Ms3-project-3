import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Forbidden
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

"""
Configuration
"""
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

ADMIN_USERNAME = "admin"


@app.route("/")
@app.route("/home")
def home():
    # Display the static home page
    return render_template("home.html")


"""
Register function
"""
@app.route("/register", methods=["GET", "POST"])
def register():
    # Register user if not already present in the DB
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
    else:
        if session.get("user"):
            # is the user already logged in?
            return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


<<<<<<< HEAD

=======
"""
Login function
"""
>>>>>>> 4f4355a569518ba5901d9bde7074d7dcb73bb949
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login function
    """
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
    else:
        if session.get("user"):
            # is the user already logged in?
            return redirect(url_for("profile", username=session["user"]))

    return render_template("login.html")


<<<<<<< HEAD

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Profile function, grab the session user's username from db
    """
=======
"""
Profile function
"""
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
>>>>>>> 4f4355a569518ba5901d9bde7074d7dcb73bb949
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    # If username match render profile.html
    if session["user"]:
        return render_template("profile.html", username=username)
    # If not redirect to login
    return redirect(url_for("login"))


<<<<<<< HEAD

=======
"""
Find notes
"""
>>>>>>> 4f4355a569518ba5901d9bde7074d7dcb73bb949
@app.route("/get_notes")
def get_notes():
    """
    Find notes
    """
    if session.get("user"):
        # Admin has acces to all notes, user sees own notes
        if session["user"] == ADMIN_USERNAME:
            notes = mongo.db.notes.find()
        else:
            notes = mongo.db.notes.find({"created_by": session["user"]})
        return render_template("notes.html", notes=notes)
    return redirect(url_for("login"))


<<<<<<< HEAD

@app.route("/logout")
def logout():
    """
    Logout function, Remove user from session cookies
    """
=======
"""
Logout function
"""
@app.route("/logout")
def logout():
    # Remove user from session cookies
>>>>>>> 4f4355a569518ba5901d9bde7074d7dcb73bb949
    if session.pop("user", None):
        flash("You have been logged out")
    return redirect(url_for("login"))


<<<<<<< HEAD

@app.route("/add_note", methods=["GET", "POST"])
def add_note():
    """
    Add notes funtion, Post the strings to mongo db
    """
=======
"""
Add notes funtion
"""
@app.route("/add_note", methods=["GET", "POST"])
def add_note():
    # Post the strings to mongo db
>>>>>>> 4f4355a569518ba5901d9bde7074d7dcb73bb949
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


<<<<<<< HEAD

@app.route("/edit_note/<note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    """
    Edit notes function, check if the user is the author of the note
    """
=======
"""
Edit notes function
"""
@app.route("/edit_note/<note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    # check if the user is the author of the note
>>>>>>> 4f4355a569518ba5901d9bde7074d7dcb73bb949
    note = mongo.db.notes.find_one({"_id": ObjectId(note_id)})
    if session["user"]:
        # Admin has acces to all notes
        if session["user"] == ADMIN_USERNAME:
            mongo.db.notes.find()
        else:
            mongo.db.notes.find({"created_by": session["user"]})
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
        return render_template("edit_note.html", note=note)
    raise Forbidden()


<<<<<<< HEAD

@app.route("/delete_note/<note_id>")
def delete_note(note_id):
    """
    Delete function, check if the user is the author of the note
    """
=======
"""
Delete function
"""
@app.route("/delete_note/<note_id>")
def delete_note(note_id):
    # check if the user is the author of the note
>>>>>>> 4f4355a569518ba5901d9bde7074d7dcb73bb949
    mongo.db.notes.find_one({"_id": ObjectId(note_id)})
    if session["user"]:
        # Admin has access to delete notes
        if session["user"] == ADMIN_USERNAME:
            mongo.db.notes.find()
        else:
            mongo.db.notes.find({"created_by": session["user"]})
        # Remove ObjectId from mongo db
        mongo.db.notes.remove({"_id": ObjectId(note_id)})
        flash("Note Deleted!")
        return redirect(url_for("get_notes"))
    raise Forbidden()


<<<<<<< HEAD

=======
"""
Error Handlers
"""
>>>>>>> 4f4355a569518ba5901d9bde7074d7dcb73bb949
@app.errorhandler(Exception)
def generic_exception_handler(e):
    """
    Error Handlers
    """
    print(e)
    return render_template("error_handlers/error.html",
                           **{"error_message": "The server does not support, or refuses to support, the major version of HTTP that was used in the request message.",
                            "error_title": "Internal Server error",
                            "error_code": 500}), 500


<<<<<<< HEAD

=======
>>>>>>> 4f4355a569518ba5901d9bde7074d7dcb73bb949
@app.errorhandler(403)
def forbidden(e):
    """
    Error Handlers
    """
    return render_template("error_handlers/error.html",
                           **{"error_message": "You don't have permisson to access on this server.",
                            "error_title": "Forbidden",
                            "error_code": 403}), 403


@app.errorhandler(404)
def not_found(e):
    return render_template("error_handlers/error.html",
                           **{"error_message": "Sorry, the page you requested could not be found.",
                            "error_title": "Not Found",
                            "error_code": 404}), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
