from flask import render_template, flash, redirect, url_for

from security import db
from security.forms.User import Create
from security.models.User import User


def create():
    form = Create.Form()
    users = User.query.all()
    if form.validate_on_submit():
        user = User(name=form.name.data, license_plate=form.license_plate.data)
        db.session.add(user)
        db.session.commit()
        flash('User has been created', 'success')
        return redirect(url_for('user'))
    return render_template('user.html', title='Register', form=form, users=users)
