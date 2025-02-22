import dlib
import cv2

class Monitor:
    def _init_(self):
        self.suspicious_logs = []
        self.is_running = False
        self.detector = dlib.get_frontal_face_detector()  # Using dlib for face detection

    def start_monitoring(self):
        self.is_running = True

    def stop_monitoring(self):
        self.is_running = False

    def check_activity(self):
        if not self.is_running:
            return False, ""

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return False, ""

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        if len(faces) > 1:
            self.suspicious_logs.append("Multiple faces detected.")
            return True, "Multiple faces detected"

        return False, ""

    def get_logs(self):
        return self.suspicious_logs