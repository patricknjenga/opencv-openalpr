import pickle

import cv2
import face_recognition
import numpy as np

from security.controllers import MainController
from security.models.User import User


class FaceID:
    process_this_frame, authorized_users, user_images = True, dict(), dict()
    frame, rgb_small_frame, face_names, face_locations = None, None, [], []

    def __init__(self) -> None:
        super().__init__()
        # self.camera = cv2.VideoCapture("D:\\others\\20191125_141101.mp4")
        self.camera = cv2.VideoCapture(0)

    def get_encodings(self):
        self.authorized_users = MainController.vehicle_id.authorized_users
        for user in self.authorized_users.keys():
            user = User.query.get(user)
            if user:
                for image in user.images:
                    self.user_images[image.user.id] = pickle.loads(image.encoding)

    def main(self, x=0):
        while True:
            self.get_encodings()
            self.get_frame()
            if x % 30 == 1:
                self.face_id()
            x = x + 1
            self.mark_faces()

    def face_id(self):
        self.face_locations = face_recognition.face_locations(self.rgb_small_frame)
        face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(list(self.user_images.values()), face_encoding, tolerance=0.60)
            if True in matches:
                # distance = face_recognition.face_distance(list(self.user_images.values()), face_encoding)
                self.face_names = list(self.authorized_users.values())[matches.index(True)][1]  # + str(int((1 - distance) * 100))
            else:
                self.face_names = 'unknown'

    def get_frame(self):
        _, self.frame = self.camera.read()
        if self.frame is not None:
            self.rgb_small_frame = cv2.resize(self.frame, (0, 0), fx=0.5, fy=0.5)
            # self.rgb_small_frame = self.frame

    def mark_faces(self):
        for (top, right, bottom, left) in np.array(self.face_locations) * 2:
            if self.face_names == 'unknown':
                cv2.UMat(cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 1))
                cv2.UMat(cv2.rectangle(self.frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED))
                cv2.UMat(cv2.putText(self.frame, self.face_names, (left + 6, bottom - 6), cv2.QT_FONT_NORMAL, 0.5, (255, 255, 255), 2))
            else:
                cv2.UMat(cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 1))
                cv2.UMat(cv2.rectangle(self.frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED))
                cv2.UMat(cv2.putText(self.frame, self.face_names, (left + 6, bottom - 6), cv2.QT_FONT_NORMAL, 0.5, (0, 0, 0), 2))

    def print_frame(self):
        while True:
            if self.frame is not None:
                yield b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + cv2.imencode('.jpg', self.frame)[1].tostring() + b'\r\n'
