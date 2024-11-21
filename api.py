from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import cv2
import json
from datetime import datetime
from deepface import DeepFace
from scipy.spatial.distance import cosine
import uvicorn


app = FastAPI()

origins = [
    "http://localhost:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base folder for face data
BASE_FOLDER = "FaceRecords"
os.makedirs(BASE_FOLDER, exist_ok=True)


# Helper Functions
def create_folder(folder_name: str):
    """Creates a folder if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def make_serializable(obj):
    """Converts non-serializable objects to serializable forms."""
    if isinstance(obj, list):
        return [make_serializable(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (float, int, str)):
        return obj
    return obj


def save_face_embedding(photo_path: str, embedding_file: str):
    """Extracts and saves face embedding."""
    try:
        embedding = DeepFace.represent(img_path=photo_path, enforce_detection=False)
        with open(embedding_file, "w") as f:
            json.dump(make_serializable(embedding), f, indent=4)
        return embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving embedding: {str(e)}")


def compare_embeddings(live_embedding, stored_embeddings, threshold=0.4):
    """Compares live embedding with stored embeddings."""
    for user, data in stored_embeddings.items():
        stored_embedding = data["embedding"][0]["embedding"]
        similarity = 1 - cosine(live_embedding, stored_embedding)
        if similarity > (1 - threshold):
            return user, similarity, data["details"]
    return None, None, None


def load_embeddings(base_folder=BASE_FOLDER):
    """Loads all stored embeddings and user data."""
    embeddings = {}
    for user_folder in os.listdir(base_folder):
        embedding_file = os.path.join(base_folder, user_folder, "embedding.json")
        details_file = os.path.join(base_folder, user_folder, "details.json")
        if os.path.exists(embedding_file) and os.path.exists(details_file):
            with open(embedding_file, "r") as ef, open(details_file, "r") as df:
                embeddings[user_folder] = {
                    "embedding": json.load(ef),
                    "details": json.load(df),
                }
    return embeddings


# Models
class UserRegistration(BaseModel):
    name: str
    age: int
    gender: str


# Endpoints
@app.post("/register/")
def register_user(name: str = Form(...), age: int = Form(...), gender: str = Form(...)):
    """Registers a user by capturing their photo and saving details."""
    user_folder = os.path.join(BASE_FOLDER, name)
    create_folder(user_folder)

    # Save user details
    details_file = os.path.join(user_folder, "details.json")
    user_details = {"name": name, "age": age, "gender": gender}
    with open(details_file, "w") as f:
        json.dump(user_details, f, indent=4)

    # Capture photo
    camera = cv2.VideoCapture(0)
    print("Press 'Space' to capture the photo.")
    photo_path = None
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                raise HTTPException(status_code=500, detail="Failed to capture image.")
            cv2.imshow("Camera", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # Space key
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                photo_path = os.path.join(user_folder, f"{name}_{timestamp}.jpg")
                cv2.imwrite(photo_path, frame)
                break
            elif key == 27:  # Escape key
                raise HTTPException(status_code=400, detail="Photo capture cancelled.")
    finally:
        camera.release()
        cv2.destroyAllWindows()

    # Save face embedding
    embedding_file = os.path.join(user_folder, "embedding.json")
    save_face_embedding(photo_path, embedding_file)

    return {"message": "User registered successfully.", "details": user_details}


@app.post("/recognize/")
def recognize_face():
    """Recognizes a face from the webcam."""
    embeddings = load_embeddings()
    if not embeddings:
        raise HTTPException(status_code=400, detail="No registered users found.")

    # Capture a frame
    camera = cv2.VideoCapture(0)
    print("Press 'Space' to capture the face for recognition.")
    live_embedding = None
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                raise HTTPException(status_code=500, detail="Failed to capture frame.")
            cv2.imshow("Recognition", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # Space key
                # Generate live embedding
                live_embedding = DeepFace.represent(frame, enforce_detection=False, detector_backend="mtcnn")
                break
            elif key == 27:  # Escape key
                raise HTTPException(status_code=400, detail="Recognition cancelled.")
    finally:
        camera.release()
        cv2.destroyAllWindows()

    if live_embedding:
        user, similarity, details = compare_embeddings(live_embedding[0]["embedding"], embeddings)
        if user:
            return {
                "message": "Face recognized.",
                "user": details,
                "similarity": similarity,
            }
    return {"message": "No match found."}


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
