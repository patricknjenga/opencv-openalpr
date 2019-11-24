import pickle

import cv2
import face_recognition
import numpy as np

from security.controllers import MainController
from security.models.User import User


class FaceID:
    process_this_frame, authorized_users = True, dict()
    frame, small_frame, rgb_small_frame, face_names, face_locations = None, None, None, [], []

    def __init__(self) -> None:
        super().__init__()
        self.camera = cv2.VideoCapture(0)

    def get_encodings(self):
        self.authorized_users = MainController.vehicle_id.authorized_users
        for user in self.authorized_users.keys():
            user = User.query.get(user)
            for image in user.images:
                self.authorized_users[image.user.id] = pickle.loads(image.encoding)

    def main(self):
        while True:
            self.get_encodings()
            self.get_frame()
            self.face_id()
            self.mark_faces()
            yield b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + cv2.imencode('.jpg', self.frame)[1].tostring() + b'\r\n'

    def face_id(self):
        self.face_locations = face_recognition.face_locations(self.rgb_small_frame)
        face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(list(self.authorized_users.values()), face_encoding, tolerance=0.75)
            if True in matches:
                user = User.query.get(list(self.authorized_users.keys())[matches.index(True)])
                self.face_names.append(user.name)
            else:
                self.face_names.append("unknown")

    def get_frame(self):
        _, frame = self.camera.read()
        self.frame = cv2.UMat(frame).get()
        self.small_frame = cv2.UMat(cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)).get()
        self.rgb_small_frame = cv2.UMat(self.small_frame[:, :, ::-1]).get()

    def mark_faces(self):
        for (top, right, bottom, left), name in zip(np.array(self.face_locations) * 4, self.face_names):
            if name == 'unknown':
                cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 1)
                cv2.rectangle(self.frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(self.frame, name, (left + 6, bottom - 6), cv2.QT_FONT_NORMAL, 0.5, (255, 255, 255), 1)
            else:
                cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 1)
                cv2.rectangle(self.frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(self.frame, name, (left + 6, bottom - 6), cv2.QT_FONT_NORMAL, 0.5, (0, 0, 0), 1)
