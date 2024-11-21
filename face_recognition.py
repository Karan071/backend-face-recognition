import cv2
import os
import json
from datetime import datetime
from deepface import DeepFace
import numpy as np


def create_folder(folder_name):
    """Creates a folder if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def make_serializable(obj):
    """Converts non-serializable objects to serializable forms."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.generic):  # For numpy scalar types like float32
        return obj.item()
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(i) for i in obj]
    return obj


def get_user_details():
    """Captures user details from input."""
    print("Enter the following details:")
    name = input("Name: ").strip()
    age = input("Age: ").strip()
    gender = input("Gender: ").strip()
    return {"name": name, "age": age, "gender": gender}


def capture_photo(name):
    """Captures a photo using the webcam."""
    camera = cv2.VideoCapture(0)
    print("Press 'Space' to capture the photo.")

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture image. Exiting...")
            break

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Space key
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"
            file_path = os.path.join("FaceRecords", name, filename)
            cv2.imwrite(file_path, frame)
            print(f"Photo saved as {file_path}")
            camera.release()
            cv2.destroyAllWindows()
            return file_path

        elif key == 27:  # Escape key
            print("Photo capture cancelled.")
            break

    camera.release()
    cv2.destroyAllWindows()
    return None


def save_face_embedding(photo_path, embedding_file):
    """Extracts and saves face embedding."""
    try:
        embedding = DeepFace.represent(img_path=photo_path, enforce_detection=False)
        with open(embedding_file, "w") as f:
            json.dump(make_serializable(embedding), f, indent=4)
        print(f"Embedding saved in {embedding_file}")
    except Exception as e:
        print(f"Error saving face embedding: {e}")


def main():
    """Main function to capture user details, photo, and save embeddings."""
    base_folder = "FaceRecords"
    create_folder(base_folder)

    # Step 1: Capture user details
    user_details = get_user_details()
    user_folder = os.path.join(base_folder, user_details["name"])
    create_folder(user_folder)

    # Step 2: Save user details
    details_file = os.path.join(user_folder, "details.json")
    with open(details_file, "w") as f:
        json.dump(user_details, f, indent=4)
    print(f"Details saved in {details_file}")

    # Step 3: Capture a photo
    photo_path = capture_photo(user_details["name"])

    # Step 4: Save face embedding
    if photo_path:
        embedding_file = os.path.join(user_folder, "embedding.json")
        save_face_embedding(photo_path, embedding_file)


if __name__ == "__main__":
    main()
