import pickle

import cv2
import face_recognition
import numpy as np

from security.models.Image import Image


def get_encodings(known_face_encodings, known_face_names):
    for image in Image.query.all():
        known_face_encodings.append(pickle.loads(image.encoding))
        known_face_names.append(image.user.name)
    return known_face_encodings, known_face_names


def face_identification():
    process_this_frame = True
    known_face_encodings = []
    known_face_names = []

    camera = cv2.VideoCapture(0)
    known_face_encodings, known_face_names = get_encodings(known_face_encodings, known_face_names)
    while True:
        frame, small_frame, rgb_small_frame = get_frame(camera)
        face_names, face_locations = face_id(process_this_frame, rgb_small_frame, known_face_encodings,
                                             known_face_names)
        frame = mark_faces(face_locations, face_names, frame)
        yield (b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + cv2.imencode('.jpg', frame)[
            1].tostring() + b'\r\n')


def face_id(process_this_frame, rgb_small_frame, known_face_encodings, known_face_names):
    global face_names, face_locations
    if process_this_frame:
        face_names = []
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.75)
            # distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            name = ""
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            face_names.append(name)
    process_this_frame = not process_this_frame
    return face_names, face_locations


def get_frame(camera):
    _, frame = camera.read()
    frame = cv2.UMat(frame).get()
    small_frame = cv2.UMat(cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)).get()
    rgb_small_frame = cv2.UMat(small_frame[:, :, ::-1]).get()
    return frame, small_frame, rgb_small_frame


def mark_faces(face_locations, face_names, frame):
    for (top, right, bottom, left), name in zip(np.array(face_locations) * 4, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
    return frame
