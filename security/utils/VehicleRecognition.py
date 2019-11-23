import sys

import cv2
from openalpr import Alpr


def vehicle_recognition():
    alpr = load_alpr()
    camera = cv2.VideoCapture(1)
    while True:
        camera, alpr, frame, plate, confidence = license_plate_recognition(camera, alpr)
        yield (b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tostring() + b'\r\n')


def load_alpr():
    region = 'us'
    configuration = 'C:\\OpenALPR\\Agent\\etc\\openalpr\\openalpr.conf'
    runtime = 'C:\\OpenALPR\\Agent\\usr\\share\\openalpr\\runtime_data'
    alpr = Alpr(region, configuration, runtime)

    if not alpr.is_loaded():
        print('Error loading OpenALPR')
        sys.exit(1)

    return alpr


def license_plate_recognition(camera, alpr, detect=True):
    plate, confidence = None, None
    _, frame = camera.read()
    result = alpr.recognize_ndarray(frame).get('results')

    if detect and result:
        plate, confidence, _, _, _, _, _, _, coordinates, vehicle_region, _ = result[0].values()
        tl, tr, br, bl = coordinates
        cv2.rectangle(frame, (tl['x'], tl['y']), (br['x'], br['y']), (0, 0, 255), 2)

    return camera, alpr, frame, plate, confidence
