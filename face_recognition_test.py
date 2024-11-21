import cv2
import os
import json
from deepface import DeepFace
from scipy.spatial.distance import cosine


def load_embeddings(base_folder="FaceRecords"):
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
    print(f"Loaded {len(embeddings)} embeddings for recognition.")
    return embeddings


def compare_embeddings(live_embedding, stored_embeddings, threshold=0.6):
    """Compares live embedding with stored embeddings."""
    best_match = None
    highest_similarity = 0

    for user, data in stored_embeddings.items():
        stored_embedding = data["embedding"][0]["embedding"]
        similarity = 1 - cosine(live_embedding, stored_embedding)

        if similarity > highest_similarity and similarity > (1 - threshold):
            highest_similarity = similarity
            best_match = (user, similarity, data["details"])

    return best_match


def realtime_face_recognition():
    """Perform real-time face recognition."""
    embeddings = load_embeddings()
    if not embeddings:
        print("No embeddings found. Please register users using main.py first.")
        return

    camera = cv2.VideoCapture(0)
    print("Press 'Q' to quit the video stream.")

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame.")
            break

        try:
            # Extract embedding for the current frame
            live_embedding = DeepFace.represent(frame, enforce_detection=False, detector_backend="mtcnn")
            if live_embedding:
                match = compare_embeddings(live_embedding[0]["embedding"], embeddings)
                if match:
                    user, similarity, details = match
                    text = (
                        f"Match: {details['name']}, "
                        f"Age: {details['age']}, "
                        f"Similarity: {similarity:.2f}"
                    )
                else:
                    text = "No match found."
                cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        except Exception as e:
            print(f"Error during recognition: {e}")

        # Show the video feed
        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    realtime_face_recognition()
