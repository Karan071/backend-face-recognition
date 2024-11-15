import face_recognition
import numpy as np


def generate_face_embedding(photo: str) -> bytes:
    """Generate the facial embedding from the provided image."""
    # Assuming the photo is a base64 string or file path
    image = face_recognition.load_image_file(photo)
    encoding = face_recognition.face_encodings(image)
    if len(encoding) > 0:
        return np.array(encoding[0]).tobytes()  # Store the first encoding
    else:
        raise Exception("No face found in the image")


def compare_faces(captured_embedding: bytes, stored_embedding: bytes) -> float:
    """Compare the captured face embedding with the stored one."""
    captured_embedding = np.frombuffer(captured_embedding, dtype=np.float64)
    stored_embedding = np.frombuffer(stored_embedding, dtype=np.float64)
    
    return np.linalg.norm(captured_embedding - stored_embedding)  # Euclidean distance, or use cosine similarity
