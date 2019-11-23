from flask import render_template

from security.utils.FaceRecognition import face_identification
from security.utils.VehicleRecognition import vehicle_recognition


def main():
    return render_template('index.html')


def face_camera():
    for frame in face_identification():
        yield (frame)


def vehicle_camera():
    for frame in vehicle_recognition():
        yield (frame)
