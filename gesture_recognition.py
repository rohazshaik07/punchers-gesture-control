import cv2
import mediapipe as mp
import numpy as np
import logging
from enum import Enum, auto

class Role(Enum):
    LEFT = auto()
    RIGHT = auto()
    TWO_PLAYER = auto()

class Gesture(Enum):
    LEFT_JAB = auto()
    RIGHT_JAB = auto()
    LEAN_DOWN = auto()
    LEAN_UP = auto()

class GestureRecognizer:
    def __init__(self, role: Role):
        self.role = role
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam.")

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False, min_detection_confidence=0.6, min_tracking_confidence=0.6
        )
        self.mp_draw = mp.solutions.drawing_utils
        logging.info("GestureRecognizer initialized.")

    def close(self):
        if self.cap:
            self.cap.release()
        self.pose.close()
        logging.info("Resources released.")

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                logging.warning("Failed to grab frame from webcam.")
                continue
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)
            gestures = []
            if results.pose_landmarks:
                gestures = self.detect_single_player(results.pose_landmarks)
                self.mp_draw.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            yield gestures, frame

    def detect_single_player(self, landmarks_proto):
        lm = landmarks_proto.landmark
        gestures = []

        NOSE = 0
        LEFT_SHOULDER, RIGHT_SHOULDER = 11, 12
        LEFT_ELBOW, RIGHT_ELBOW = 13, 14
        LEFT_WRIST, RIGHT_WRIST = 15, 16
        LEFT_HIP, RIGHT_HIP = 23, 24

        def get_angle(a, b, c):
            a = np.array([a.x, a.y])
            b = np.array([b.x, b.y])
            c = np.array([c.x, c.y])
            ba = a - b
            bc = c - b
            cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
            return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

        # === LEAN DOWN: Both wrists below hips, elbows below shoulders ===
        left_wrist_down = lm[LEFT_WRIST].y > lm[LEFT_HIP].y + 0.02
        right_wrist_down = lm[RIGHT_WRIST].y > lm[RIGHT_HIP].y + 0.02
        left_elbow_down = lm[LEFT_ELBOW].y > lm[LEFT_SHOULDER].y + 0.02
        right_elbow_down = lm[RIGHT_ELBOW].y > lm[RIGHT_SHOULDER].y + 0.02

        if left_wrist_down and right_wrist_down and left_elbow_down and right_elbow_down:
            gestures.append(Gesture.LEAN_DOWN)

        # === LEAN UP: Both wrists above shoulders and near head ===
        left_wrist_up = (lm[LEFT_WRIST].y < lm[LEFT_SHOULDER].y) and (abs(lm[LEFT_WRIST].x - lm[NOSE].x) < 0.13)
        right_wrist_up = (lm[RIGHT_WRIST].y < lm[RIGHT_SHOULDER].y) and (abs(lm[RIGHT_WRIST].x - lm[NOSE].x) < 0.13)
        left_elbow_high = lm[LEFT_ELBOW].y < lm[LEFT_SHOULDER].y + 0.08
        right_elbow_high = lm[RIGHT_ELBOW].y < lm[RIGHT_SHOULDER].y + 0.08
        if left_wrist_up and right_wrist_up and left_elbow_high and right_elbow_high:
            gestures.append(Gesture.LEAN_UP)

        # Left Jab
        left_jab_angle = get_angle(lm[LEFT_SHOULDER], lm[LEFT_ELBOW], lm[LEFT_WRIST])
        if 150 < left_jab_angle < 185 and lm[LEFT_WRIST].y < lm[LEFT_ELBOW].y:
            gestures.append(Gesture.LEFT_JAB)
        # Right Jab
        right_jab_angle = get_angle(lm[RIGHT_SHOULDER], lm[RIGHT_ELBOW], lm[RIGHT_WRIST])
        if 150 < right_jab_angle < 185 and lm[RIGHT_WRIST].y < lm[RIGHT_ELBOW].y:
            gestures.append(Gesture.RIGHT_JAB)

        return gestures