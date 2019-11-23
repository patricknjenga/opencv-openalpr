from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user

from security import db, bcrypt
from security.forms.Admin import Register, Login
from security.models.Admin import Admin


def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Register.Form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Admin(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login.Form()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Register', form=form)


def logout():
    logout_user()
    return redirect(url_for('home'))
