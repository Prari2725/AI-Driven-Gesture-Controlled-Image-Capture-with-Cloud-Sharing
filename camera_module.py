import cv2

class CameraManager:
    def __init__(self, camera_index=0):
        """
            Initializes the CameraManager object.

            Parameters:
                camera_index (int): The index of the camera to be used. Default is 0.

            Returns:
                None
        """

        self.camera_index = camera_index
        self.cap = None
    
    def open_camera(self):
        """
            Opens the camera using the camera_index parameter.

            Parameters:
                None

            Returns:
                None
        """
        
        self.cap = cv2.VideoCapture(self.camera_index)
    
    def read_frame(self):
        """
            Reads a frame from the camera and returns it.

            Returns:
                numpy.ndarray or None: The captured frame from the camera if successful, None otherwise.
        """

        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                print("Failed to capture frame from camera.")
                return None
        else:
            print("Camera is not opened yet.")
            return None
    
    def release_camera(self):
        """
            Release the camera.

            This function releases the camera and sets the `cap` attribute to None.

            Parameters:
                None

            Returns:
                None
        """

        if self.cap is not None:
            self.cap.release()
            self.cap = None

# In main.py, you would use the CameraManager class like this:

# from camera_module import CameraManager
if __name__ == "__main__":
    camera_manager = CameraManager()
    camera_manager.open_camera()
    frame = camera_manager.read_frame()
    if frame is not None:
        pass
    cv2.imshow("frame",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    camera_manager.release_camera()
