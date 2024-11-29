from camera_module import CameraManager
from hand_tracking_module import HandTracker
from google_drive_module import DriveService
from qrcode_module import QRCodeGenerator

from datetime import datetime
from PIL import Image
import numpy as np
import time
import cv2 
import os


camera_manager = CameraManager()
camera_manager.open_camera()
qrcode_generator = QRCodeGenerator()
hand_tracker = HandTracker(detection_confidence=0.8, max_hands=2)
parent_folder_id = '1QvD0Mf6GplCMz2DGo66yy80eVPG4gWsN'
drive_service = DriveService(parent_folder_id)

cap_window_name = 'Capture Image!'
upload_window_name = 'Uploading Image to Google Drive...'
download_window_name = 'Download Now!'

main_frame = None
uploaded_image_id = None
def save_image(frame):
    # Check if the 'SavedImages' directory exists and create it if not
    saved_images_dir = 'SavedImages'
    if not os.path.exists(saved_images_dir):
        os.makedirs(saved_images_dir)

    # Format the file name with the current date and time
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = 'camera_{}.jpg'.format(date_time)
    
    # Construct the full file path
    file_path = os.path.join(saved_images_dir, file_name)
    
    # Save the image to the specified path
    cv2.imwrite(file_path, frame)
    return file_path, file_name


def draw_text_centered(image, text, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, font_thickness=2, color=(0, 0, 0)):
    # Calculate the width and height of the text box
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

    # Get the frame dimensions
    frame_height, frame_width = image.shape[:2]

    # Calculate the bottom-left corner of the text to center it
    text_x = (frame_width - text_size[0]) // 2
    text_y = (frame_height + text_size[1]) // 2
    # Calculate the position and size of the background rectangle
    bg_rect_x = text_x - 5
    bg_rect_y = text_y - text_size[1] - 5
    bg_rect_width = text_size[0] + 10
    bg_rect_height = text_size[1] + 10

    # Draw the filled white rectangle
    cv2.rectangle(image, (bg_rect_x, bg_rect_y), (bg_rect_x + bg_rect_width, bg_rect_y + bg_rect_height), (255, 255, 255), -1)

    # Draw the text on the frame
    cv2.putText(image, text, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)


def combine_frame_and_qr(frame, qr_image):
    
    qr_code = qr_image

    # Ensure both images have the same height
    frame_height, frame_width = frame.shape[:2]
    qr_height, qr_width = qr_code.shape[:2]

    # If the images do not have the same height, resize them
    if frame_height != qr_height:
        # Scale QR code to match the frame's height
        scale_factor = frame_height / qr_height
        qr_code = cv2.resize(qr_code, (int(qr_width * scale_factor), frame_height))

    # Concatenate images horizontally
    combined_image = np.hstack((frame, qr_code))

    return combined_image

import cv2
import time
# Assuming camera_manager and hand_tracker are initialized and configured elsewhere in your code


def capture():
    """Function that captures and uploads an image based on the finger count."""
    while True:
        frame = camera_manager.read_frame()
        if frame is not None:
            hands, _ = hand_tracker.find_hands(frame)
            if hands:
                finger_count = hand_tracker.get_finger_count(hands[0])
                timer_values = {
                    (0, 1, 0, 0, 0): 1,
                    (0, 1, 1, 0, 0): 2,
                    (0, 1, 1, 1, 0): 3,
                    (0, 1, 1, 1, 1): 4,
                    (1, 1, 1, 1, 1): 5
                }
                timer = timer_values.get(tuple(finger_count), None)
                if timer is not None:
                    capture_image(timer)
            cv2.imshow('frame', frame)
            #cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            key_press = cv2.waitKey(1)
            if key_press == 27 or main_frame is not None:
                cv2.destroyAllWindows()
                camera_manager.release_camera()
                break

def capture_image(timer):
    global main_frame
    """Captures an image, displays it for a short time, and uploads it to Google Drive."""
    prev = time.time()
    while timer >= 0:
        frame = camera_manager.read_frame()
        draw_text_centered(frame, f"Timer : {timer}")
        cv2.imshow('frame', frame)
        #cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.waitKey(100)
        cur = time.time()
        if cur - prev > 1:
            prev = cur
            timer -= 1
    main_frame = camera_manager.read_frame()
    #camera_manager.release_camera()
    
def upload_image():
    """Uploads an image to Google Drive."""
    global main_frame
    global uploaded_image_id
    file_path, file_name = save_image(main_frame)
    
    frame_download = main_frame.copy()
    draw_text_centered(frame_download, "Uploading Plz wait..!")
    cv2.imshow("Uploading", frame_download)
    cv2.waitKey(4000)
    uploaded_image_id = drive_service.upload_file(file_path, file_name)
    cv2.destroyWindow("Uploading")
    #cv2.setWindowProperty("Uploading", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cpy_frame_done = main_frame.copy()
    draw_text_centered(cpy_frame_done, "Uploading Done!!")
    cv2.imshow("Uploaded", cpy_frame_done)
    #cv2.setWindowProperty("Uploaded", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.waitKey(4000)
    cv2.destroyWindow("Uploaded")
    
    

def generate_qr():
    """Generates a QR code for the uploaded image."""
    global uploaded_image_id
    qr_img = qrcode_generator.generate_qr_code(f'https://drive.google.com/uc?id={uploaded_image_id}')
    qr_img = qr_img.convert('RGB')  # Convert to RGB format
    qr_img = cv2.cvtColor(np.array(qr_img), cv2.COLOR_RGB2BGR)
    cv2.imshow("QR Code", qr_img)
    start_time = time.time()
    while time.time() - start_time < 10:        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyWindow("QR Code")