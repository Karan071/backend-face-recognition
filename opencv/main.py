import cv2  # OpenCV library for image processing
import pickle  # For saving and loading data
import numpy as np  # For numerical operations
import os  # For file and directory handling


# Initialize the webcam (0 is the default webcam, 1 for an external webcam if connected)
video = cv2.VideoCapture(0)

# Load the pre-trained Haar cascade classifier for face detection
face_detect = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")

# List to store face data and a counter variable
faces_data = []
i = 0

# Prompt the user to enter their name
name = input("Enter your Name: ")

# Loop to capture frames from the webcam and process them
while True:
    # Capture a frame from the webcam
    ret, attendance_frame = video.read()
    
    # Convert the frame to grayscale (Haar cascades work on grayscale images)
    grey_scale = cv2.cvtColor(attendance_frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = face_detect.detectMultiScale(grey_scale, 1.3, 2)
    
    # Loop through all detected faces
    for (x, y, w, h) in faces:
        # Crop the detected face from the frame
        cropped_img = attendance_frame[y: y + h, x: x + w]
        
        # Resize the cropped face image to a fixed size (50x50 pixels)
        resized_img = cv2.resize(cropped_img, (50, 50))
        
        # Save every 10th frame to avoid redundancy and store only 100 face samples
        if len(faces_data) <= 100 and i % 10 == 0:
            faces_data.append(resized_img)  # Add the resized face to the list
            
        # Increment the counter
        i += 1
        
        # Display the number of captured face samples on the frame
        cv2.putText(attendance_frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        
        # Draw a rectangle around the detected face
        cv2.rectangle(attendance_frame, (x, y), (x + w, y + h), (50, 50, 255), 3)
    
    # Display the current frame in a window
    cv2.imshow('frame', attendance_frame)
    
    # Break the loop if 'q' is pressed or 100 face samples are collected
    key = cv2.waitKey(1)
    if key == ord('q') or len(faces_data) == 100:
        break

# Release the webcam and close the OpenCV window
video.release()
cv2.destroyAllWindows()

# Convert the list of face data to a NumPy array and reshape it for storage
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)

# Save or update the names data in 'data/names.pkl'
if 'names.pkl' not in os.listdir('data/'):  # Check if the names file exists
    # If not, create a new names file with the entered name repeated 100 times
    names = [name] * 100
    with open('data/names.pkl', 'wb') as file:
        pickle.dump(names, file)
else:
    # If the file exists, load the existing names, append the new name, and save it back
    with open('data/names.pkl', 'rb') as file:
        names = pickle.load(file)
    names = names + [name] * 100
    with open('data/names.pkl', 'wb') as file:
        pickle.dump(names, file)

# Save or update the face data in 'data/faces_data.pkl'
if 'faces_data.pkl' not in os.listdir('data/'):  # Check if the face data file exists
    # If not, create a new file to save the captured face data
    with open('data/faces_data.pkl', 'wb') as file:
        pickle.dump(faces_data, file)
else:
    # If the file exists, load the existing data, append the new data, and save it back
    with open('data/faces_data.pkl', 'rb') as file:
        faces = pickle.load(file)
    faces = np.append(faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as file:
        pickle.dump(faces, file)

