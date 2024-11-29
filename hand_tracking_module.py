from cvzone.HandTrackingModule import HandDetector
import cv2

class HandTracker:
    def __init__(self, detection_confidence=0.8, max_hands=2):
        """
        Initializes a new instance of the HandTracker class.

        Parameters:
            detection_confidence (float): The confidence threshold for hand detection. Default is 0.8.
            max_hands (int): The maximum number of hands to detect. Default is 2.

        Returns:
            None
        """

        self.detector = HandDetector(detectionCon=detection_confidence, maxHands=max_hands)
    
    def find_hands(self, frame, draw=True):
        """
        Finds hands in a given frame using the HandDetector object.

        Parameters:
            frame (numpy.ndarray): The frame in which to search for hands.
            draw (bool, optional): Whether to draw the detected hands on the frame. Defaults to True.

        Returns:
            tuple: A tuple containing the detected hands and the modified frame. The detected hands are represented as a list of dictionaries, where each dictionary contains information about a detected hand. The modified frame is a numpy array representing the frame with the detected hands drawn on it if draw is True. If no hands are detected, the detected hands list will be empty.
        """

        return self.detector.findHands(frame, draw=draw)
    
    def get_hand_landmarks(self, frame):
        """
        Finds the landmarks of the detected hands in a given frame.

        Parameters:
            self (HandTracker): The HandTracker object.
            frame (numpy.ndarray): The frame in which to detect the hands.

        Returns:
            list: A list of landmarks for each detected hand. Each landmark is a list of 21 landmark points.
        """

        hands, frame = self.detector.findHands(frame)
        landmarks_list = []
        if hands:
            for hand in hands:
                landmarks = hand['lmList']  # list of 21 landmark points
                landmarks_list.append(landmarks)
        return landmarks_list
    def get_finger_count(self, frame):
        """
        Finds the finger count of the detected hands in a given frame.

        Parameters:
            self (HandTracker): The HandTracker object.
            frame (numpy.ndarray): The frame in which to detect the hands.

        Returns:
            list: A list of finger counts for each detected hand. Each finger count is a list of 5 finger counts.
        """
        return self.detector.fingersUp(frame)
# In your main.py you would use the HandTracker class as follows:

# from hand_tracking_module import HandTracker
if __name__ == "__main__":
    from camera_module import CameraManager

    camera_manager = CameraManager()
    hand_tracker = HandTracker(detection_confidence=0.8, max_hands=2)

    camera_manager.open_camera()
    frame = camera_manager.read_frame()

    landmarks_list = hand_tracker.get_hand_landmarks(frame)
    print(landmarks_list)
    cv2.imshow("frame",frame)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break
    camera_manager.release_camera()
