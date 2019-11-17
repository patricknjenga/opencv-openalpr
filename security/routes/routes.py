from flask import Response, redirect, url_for
from flask_login import login_required

from security import app, db
from security.controllers import UserController, MainController, ImageController
# Main Routes
from security.controllers.MainController import get_frame


@app.route('/reset')
@login_required
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('home'))


@app.route('/')
@login_required
def home():
    return MainController.main()


# User Routes
@app.route("/register", methods=['GET', 'POST'])
def register():
    return UserController.register()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return UserController.login()


@app.route('/logout')
@login_required
def logout():
    return UserController.logout()


# Image Routes
@app.route("/image", methods=['GET', 'POST'])
@login_required
def image():
    return ImageController.create()


@app.route("/gallery", methods=['GET', 'POST'])
@login_required
def gallery():
    return ImageController.gallery()


@app.route('/calc')
@login_required
def calc():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
