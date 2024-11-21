from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime
from deepface import DeepFace
from scipy.spatial.distance import cosine
import uvicorn
 
app = FastAPI()
 
# Enable CORS for frontend access
origins = [
    "http://localhost:5174",  # React development server URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
BASE_FOLDER = "FaceRecords"
os.makedirs(BASE_FOLDER, exist_ok=True)
 
# Helper Functions
def save_face_embedding(photo_path: str, embedding_file: str):
    """Extracts and saves face embedding."""
    try:
        embedding = DeepFace.represent(img_path=photo_path, enforce_detection=False)
        with open(embedding_file, "w") as f:
            json.dump(embedding, f, indent=4)
        return embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving embedding: {str(e)}")
 
 
@app.post("/register/")
async def register_user(
    name: str = Form(...), age: int = Form(...), gender: str = Form(...), photo: UploadFile = None
):
    """Registers a user by saving the uploaded photo and details."""
    user_folder = os.path.join(BASE_FOLDER, name)
    os.makedirs(user_folder, exist_ok=True)
 
    # Save user details
    details_file = os.path.join(user_folder, "details.json")
    user_details = {"name": name, "age": age, "gender": gender}
    with open(details_file, "w") as f:
        json.dump(user_details, f, indent=4)
 
    # Save uploaded photo
    photo_path = os.path.join(user_folder, "photo.jpg")
    with open(photo_path, "wb") as f:
        f.write(await photo.read())
 
    # Save face embedding
    embedding_file = os.path.join(user_folder, "embedding.json")
    save_face_embedding(photo_path, embedding_file)
 
    return {"message": "User registered successfully.", "details": user_details}
 
 
@app.post("/recognize/")
async def recognize_face(photo: UploadFile):
    """Recognizes a face by comparing uploaded photo with saved embeddings."""
    # Save uploaded photo temporarily
    temp_photo_path = "temp_photo.jpg"
    with open(temp_photo_path, "wb") as f:
        f.write(await photo.read())
 
    # Generate embedding for uploaded photo
    try:
        live_embedding = DeepFace.represent(img_path=temp_photo_path, enforce_detection=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embedding: {str(e)}")
 
    # Load existing embeddings
    embeddings = load_embeddings()
    for user, data in embeddings.items():
        stored_embedding = data["embedding"][0]["embedding"]
        similarity = 1 - cosine(live_embedding[0]["embedding"], stored_embedding)
        if similarity > 0.6:  # Threshold
            return {"message": "Face recognized.", "user": data["details"], "similarity": similarity}
 
    return {"message": "No match found."}
 
 
def load_embeddings(base_folder=BASE_FOLDER):
    """Loads stored embeddings from disk."""
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
 
 
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
