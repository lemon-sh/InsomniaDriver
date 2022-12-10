import time

import mediapipe as mp

import maths


class DrowsyDetector:
    def __init__(self):
        self._eye_idxs = {"left": [362, 385, 387, 263, 373, 380], "right": [33, 160, 158, 133, 153, 144], }
        self._start_time = time.perf_counter()
        self._facemesh_model = mp.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                                                               min_detection_confidence=0.5,
                                                               min_tracking_confidence=0.5)

        self.drowsy_time = 0.0
        self.eyes_closed = False
        self.alarm = False
        self.ear = 0.0
        self.coordinates = None
        self.detection = False

    def feed(self, frame, ear_thresh, wait_time_thresh):
        frame.flags.writeable = False
        frame_h, frame_w, _ = frame.shape
        results = self._facemesh_model.process(frame)

        if results.multi_face_landmarks:
            self.detection = True
            landmarks = results.multi_face_landmarks[0].landmark
            self.ear, self.coordinates = maths.calculate_avg_ear(landmarks, self._eye_idxs["left"],
                                                                 self._eye_idxs["right"],
                                                                 frame_w, frame_h)

            if self.ear < ear_thresh:
                end_time = time.perf_counter()

                self.drowsy_time += end_time - self._start_time
                self._start_time = end_time
                self.eyes_closed = True

                if self.drowsy_time >= wait_time_thresh:
                    self.alarm = True
                return
        else:
            self.detection = False

        self._start_time = time.perf_counter()
        self.drowsy_time = 0.0
        self.eyes_closed = False
        self.alarm = False
