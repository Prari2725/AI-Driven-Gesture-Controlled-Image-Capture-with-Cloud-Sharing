import cv2
import datetime
import os

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

# Check if the 'click' folder exists, if not, create it
click_folder = 'click'
if not os.path.exists(click_folder):
    os.makedirs(click_folder)

# Count the number of existing 'clk' folders to determine the new folder name
clk_folders = [folder for folder in os.listdir(click_folder) if folder.startswith('clk')]
new_folder_name = f'clk{len(clk_folders) + 1}'

# Create a new folder for this run
os.makedirs(os.path.join(click_folder, new_folder_name))

# Text settings
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
thickness = 2

# Initialize a dictionary to keep track of smile status for each face
smile_status = {}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame")
        break

    original_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Check if each face has a smile
    all_smiles = True
    for i, (x, y, w, h) in enumerate(faces):
        face_roi = gray[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(face_roi, 1.8, 20)

        # Update smile status for each face
        if len(smiles) > 0:
            smile_status[i] = True
        else:
            smile_status[i] = False

        # If any face is not smiling, set all_smiles to False
        if not smile_status[i]:
            all_smiles = False

        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Display message on frame
        if all_smiles:
            cv2.putText(frame, "Your selfie is ready to be captured!", (x, y-10), font, font_scale, (0, 255, 0), thickness)
        else:
            cv2.putText(frame, "Please smile 😊😊😊 to capture your selfie!", (x, y-10), font, font_scale, (0, 0, 255), thickness)

    # If all faces are smiling, capture the selfie
    if all_smiles and len(faces) > 0:
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file_name = f'selfie-{time_stamp}.png'
        folder_path = os.path.join(click_folder, new_folder_name)
        cv2.imwrite(os.path.join(folder_path, file_name), original_frame)
        print("Selfie captured!")
    else:
        print("Smile 😊😊😊 Please")

    # Display the frame
    cv2.imshow('Camera Frame', frame)
    
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
