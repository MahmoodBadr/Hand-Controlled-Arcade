import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def get_hand_position(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        hand_positions = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((cx, cy))
                hand_positions.append(landmarks)
                self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
        return hand_positions, frame

    def is_gesture(self, landmarks):
        # Check if the index finger and thumb are close together
        if landmarks:
            thumb_tip = landmarks[0][4]
            index_tip = landmarks[0][8]
            distance = ((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2) ** 0.5
            return distance < 30  # Adjust threshold as needed
        return False
