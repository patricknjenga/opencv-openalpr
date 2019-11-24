import cv2
from openalpr import Alpr

from security.models.User import User


class VehicleID:
    region, configuration, runtime = 'us', 'C:\\OpenALPR\\Agent\\etc\\openalpr\\openalpr.conf', 'C:\\OpenALPR\\Agent\\usr\\share\\openalpr\\runtime_data'
    frame, small_frame, detect, authorized_users, plate = None, None, True, dict(), None

    def __init__(self):
        super().__init__()
        self.alpr = Alpr(self.region, self.configuration, self.runtime)  # init alpr engine
        self.camera = cv2.VideoCapture(1)  # record frames from video source

    def main(self):
        while True:
            self.license_plate_recognition()
            frame = b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + cv2.imencode('.jpg', self.frame)[1].tostring() + b'\r\n'
            yield frame

    def get_frame(self):
        _, frame = self.camera.read()  # read from video source
        self.frame = cv2.UMat(frame).get()  # use tapi to take advantage of gpu
        self.small_frame = cv2.UMat(cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)).get()  # 1/4 scale for faster processing

    def license_plate_recognition(self):
        self.get_frame()
        result = self.alpr.recognize_ndarray(self.small_frame).get('results')  # use alpr engine to detect license plate
        if self.detect and result:
            self.plate, confidence, _, _, _, _, _, _, coordinates, vehicle_region, _ = result[0].values()  # deserialize results of license plate recognition
            tl, tr, br, bl = coordinates
            cv2.rectangle(self.frame, (tl['x'] * 4, tl['y'] * 4), (br['x'] * 4, br['y'] * 4), (0, 0, 255), 2)  # plot coordinates of license plate onto frame
            self.authorize_vehicle()  # search database for vehicle plate and obtain registered owner if present

    def authorize_vehicle(self):
        user = User.query.filter_by(license_plate=self.plate).first()  # query user that owns vehicle
        if user:
            self.authorized_users[user.id] = user.name  # load user ont authorized list on gate entry
