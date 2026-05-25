#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.get("/")
def show_welcome():
    return render_template("pages/welcome.jinja")


#-----------------------------------------------------------
# Creature list page - Show all the creatures
#-----------------------------------------------------------
@app.get("/creatures")
def show_all_creatures():
    with connect_db() as db:
        sql = """
            SELECT id, species, name
            FROM creatures
        """
        params = ()
        creatures = db.execute(sql, params).fetchall()

        return render_template("pages/creature_list.jinja", creatures=creatures)


#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")


#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.get("/user/new")
def show_signup_form():
    return render_template("pages/user_form.jinja")

#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.post("/user")
def add_user():
    forename = request.form.get('forename', '').strip()
    surname  = request.form.get('surname',  '').strip()
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = "SELECT id FROM user WHERE username=?"
        params = (username,)
        not_user = db.execute(sql, params).fetchone()

        if  not_user:
            flash(f"Username '{username}' already exists", "error")
            return redirect("/user/new")

        pass_hash = generate_password_hash(password)

        sql = """
            INSERT INTO user (forename, surname, username, pass_hash)
            VALUES (?, ?, ?, ?)
        """
        params = (forename, surname, username, pass_hash)
        db.execute(sql, params)

        flash("Account created. Please login", "success")
        return redirect("/login_page")
    

    # lgoin
@app.get("/login_page")
def show_login_form():
    return render_template("pages/login_form.jinja")



@app.post("/login")
def login_user():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = """
            SELECT id, forename, surname, pass_hash, is_admin
            FROM user
            WHERE username=?
        """
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if not user:
            flash(f"Unknown user", "error")
            return redirect("/login_page")

        if not check_password_hash(user["pass_hash"], password):
            flash(f"Incorrect password", "error")
            return redirect("/login_page")

        session["logged_in"] = True
        session["user"] = {
            "id": user["id"],
            "username": username,
            "forename": user["forename"],
            "surname":  user["surname"],
            "admin": user["is_admin"]
        }

        flash("Login successful", "success")
        return redirect("/")
    

@app.get("/admin")
@login_required
def admin_page():
    return render_template("pages/adminPage.jinja")
    ...

@app.get("/logout")
def logout_admin():
    session.clear()
    flash(f"You have been logged out", "success")
    return redirect("/")

@app.post("/minion_name")
def get_minion_name():
        return render_template("pages/mionName.jinja")



@app.get("/message_new")
@login_required
def show_message_form():
    return render_template("pages/message_form.jinja")

@app.post("/message")
def add_message():
    user = session["user"]
    id = user["id"]
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()

    with connect_db() as db:
        sql = """
            INSERT INTO message (user_id, title, body)
            VALUES (?, ?, ?)
        """
        params = (id, title, body)
        db.execute(sql, params)
    
        

        flash("message posted!!", "success")
        return redirect("/")
    

@app.get("/messages")
def show_messages():
    with connect_db() as db:
        sql = """
        SELECT *
        FROM message
        JOIN user ON message.user_id=user.id

""" 
        messages = db.execute(sql).fetchall()
    return render_template("pages/messages.jinja", message=messages)
        
@app.get(f"/message/<int:id>/edit")
@login_required
def show_edit_message_form(id):
    with connect_db() as db:
        sql = """
            SELECT id, title, body, user_id FROM message WHERE id=?
        """
        params = (id,)
        message = db.execute(sql, params).fetchone()

        if message and message["user_id"] == session["user"]["id"]:
            return render_template("pages/message_edit_form.jinja", message=message)

        flash("Invalid message", "error")
        return redirect("/messages")
    
@app.post("/message/<int:id>/update")
@login_required
def process_edited_message(id):
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()

    user_id = session["user"]["id"]

    with connect_db() as db:
        sql = """
            UPDATE message SET
                title = ?,
                body = ?
            WHERE id = ? AND user_id = ?
        """
        params = (title, body, id, user_id)
        db.execute(sql, params)

        flash("Message updated", "success")
        return redirect("/messages")



@app.get(f"/message/<int:id>/delete")
@login_required
def process_delete_message(id):
    with connect_db() as db:
        sql = """
            SELECT user_id FROM message WHERE id=?
        """
        params = (id,)
        message = db.execute(sql, params).fetchone()

        if message and message["user_id"] == session["user"]["id"]:

            sql = """
                DELETE FROM message WHERE id=?
            """
            params = (id,)
            db.execute(sql, params)

            flash("Message deleted", "success")
            return redirect("/messages")

        flash("Invalid message", "error")
        return redirect("/messages")
    