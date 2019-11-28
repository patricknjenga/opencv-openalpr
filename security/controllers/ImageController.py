import os
import pickle
import secrets

import face_recognition
from PIL import Image
from flask import flash, render_template, redirect, url_for

from security import app, db
from security.forms.Image import Create
from security.models.Image import Image as ImageModel
from security.models.User import User


def create(user):
    user = User.query.get(user)
    images = ImageModel.query.filter_by(user=user).all()
    form = Create.Form()

    if form.validate_on_submit():
        if form.picture.raw_data:
            picture_path = save_picture(form.picture.data)
            picture = face_recognition.load_image_file(form.picture.data)
            picture_encoding = face_recognition.face_encodings(picture)
            if picture_encoding:
                image = ImageModel(file=picture_path, encoding=pickle.dumps(picture_encoding[0]), user=user)
                db.session.add(image)
                db.session.commit()
                flash('Image saved', 'success')
            else:
                flash('Face Cannot be Identified', 'danger')
            return redirect(url_for('image', user_id=user.id))

    return render_template('image.html', title='Store Image', form=form, user=user, images=images)


def save_picture(form_picture):
    random_hex = secrets.token_hex(20)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture)
    image = Image.open(form_picture)
    image.save(picture_path)
    return picture
