from flask import Response, redirect, url_for
from flask_login import login_required

from security import app, db
from security.controllers import AdminController, MainController, ImageController, UserController


@app.route('/reset')
@login_required
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('home'))


# Main Routes
@app.route('/')
@login_required
def home():
    return MainController.main()


# Admin Routes
@app.route("/register", methods=['GET', 'POST'])
def register():
    return AdminController.register()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return AdminController.login()


@app.route('/logout')
@login_required
def logout():
    return AdminController.logout()


# User Routes
@app.route("/user", methods=['GET', 'POST'])
@login_required
def user():
    return UserController.create()


# Image Routes
@app.route("/user/<user_id>/image", methods=['GET', 'POST'])
@login_required
def image(user_id):
    return ImageController.create(user_id)


@app.route('/camera_1')
@login_required
def camera_1():
    return Response(MainController.face_id.main(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera_2')
@login_required
def camera_2():
    return Response(MainController.vehicle_id.main(), mimetype='multipart/x-mixed-replace; boundary=frame')
