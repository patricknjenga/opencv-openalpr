from flask import Response, redirect, url_for
from flask_login import login_required

from security import app, db
from security.controllers import AdminController, MainController, ImageController, UserController
from security.controllers.MainController import face_camera, vehicle_camera


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
@app.route("/create", methods=['GET', 'POST'])
def create():
    return UserController.create()


# Image Routes
@app.route("/user/<user>/image", methods=['GET', 'POST'])
@login_required
def image(user):
    return ImageController.create(user)


@app.route('/camera1')
@login_required
def camera_1():
    return Response(vehicle_camera(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera2')
@login_required
def camera_2():
    return Response(face_camera(), mimetype='multipart/x-mixed-replace; boundary=frame')
