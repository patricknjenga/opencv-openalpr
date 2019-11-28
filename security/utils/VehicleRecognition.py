import queue

import cv2
from openalpr import Alpr

from security import socketio
from security.models.User import User


class VehicleID:
    region, configuration, runtime = 'us', 'C:\\OpenALPR\\Agent\\etc\\openalpr\\openalpr.conf', 'C:\\OpenALPR\\Agent\\usr\\share\\openalpr\\runtime_data'
    frame, small_frame, detect, authorized_users, plate, queue = None, None, True, dict(), None, queue.Queue(1000)

    def __init__(self):
        super().__init__()
        self.alpr = Alpr(self.region, self.configuration, self.runtime)  # init alpr engine
        # self.camera = cv2.VideoCapture("D:\\others\\20191125_141145.mp4")  # record frames from video source
        self.camera = cv2.VideoCapture(1)  # record frames from video source

    def main(self):
        while True:
            self.get_frame()
            self.license_plate_recognition()

    def get_frame(self):
        _, frame = self.camera.read()  # read from video source
        self.frame = cv2.UMat(frame).get()  # use tapi to take advantage of gpu
        self.small_frame = cv2.UMat(cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)).get()  # 1/4 scale for faster processing

    def license_plate_recognition(self):
        if self.small_frame is not None:
            result = self.alpr.recognize_ndarray(self.small_frame).get('results')  # use alpr engine to detect license plate
            if self.detect and result:
                self.plate, confidence, _, _, _, _, _, _, coordinates, vehicle_region, _ = result[0].values()  # deserialize results of license plate recognition
                tl, tr, br, bl = coordinates
                cv2.UMat(cv2.rectangle(self.frame, (tl['x'] * 4, tl['y'] * 4), (br['x'] * 4, br['y'] * 4), (0, 255, 255), 8))  # plot coordinates of license plate onto frame
                cv2.UMat(cv2.rectangle(self.frame, (bl['x'] * 4, bl['y'] * 4), (br['x'] * 4, br['y'] * 4 + 25), (0, 255, 255), cv2.FILLED))
                cv2.UMat(cv2.putText(self.frame, self.plate, (bl['x'] * 4 + 40, bl['y'] * 4 + 15), cv2.QT_FONT_NORMAL, 0.7, (0, 0, 0), 2))
                self.authorize_vehicle()  # search database for vehicle plate and obtain registered owner if present

    def authorize_vehicle(self):
        user = User.query.filter_by(license_plate=self.plate).first()  # query user that owns vehicle
        if user:
            self.authorized_users[user.id] = [user.id, user.name, user.license_plate]  # load user ont authorized list on gate entry
            socketio.emit('message', self.authorized_users)

    def print_frame(self):
        while True:
            if self.frame is not None:
                yield b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + cv2.imencode('.jpg', self.frame)[1].tostring() + b'\r\n'
