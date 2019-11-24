from flask import render_template

from security.utils.FaceRecognition import FaceID
from security.utils.VehicleRecognition import VehicleID

vehicle_id = VehicleID()
face_id = FaceID()


def main():
    return render_template('index.html')
