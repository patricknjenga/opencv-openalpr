import sys

import cv2
from openalpr import Alpr


def vehicle_recognition():
    alpr = Alpr("us", 'C:\\OpenALPR\\Agent\\etc\\openalpr\\openalpr.conf',
                'C:\\OpenALPR\\Agent\\usr\\share\\openalpr\\runtime_data')
    camera = cv2.VideoCapture(1)
    alpr_available(alpr)

    while True:
        _, frame = camera.read()
        yield (b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + cv2.imencode('.jpg', frame)[
            1].tostring() + b'\r\n')
        result = alpr.recognize_ndarray(frame).get('results')
        plate, confidence, matches_template, plate_index, region, region_confidence, processing_time_ms, requested_topn, coordinates, vehicle_region, candidates = result
        print(plate)


def alpr_available(alpr):
    if not alpr.is_loaded():
        print('Error loading OpenALPR')
        sys.exit(1)
