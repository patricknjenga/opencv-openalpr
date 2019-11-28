import threading

from flask import render_template

from security.utils.FaceRecognition import FaceID
from security.utils.VehicleRecognition import VehicleID

vehicle_id = VehicleID()
face_id = FaceID()


def index():
    thread = threading.Thread(target=face_id.main)
    thread.start()
    thread = threading.Thread(target=vehicle_id.main)
    thread.start()
    return render_template('index.html')


def face():
    for frame in face_id.print_frame():
        yield frame


def vehicle():
    for frame in vehicle_id.print_frame():
        yield frame
