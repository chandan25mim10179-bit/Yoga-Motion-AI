import cv2
import numpy as np

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.pose_engine import PoseEngine
from backend.yoga_analyzer import YogaAnalyzer


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Yoga Motion AI",
    description=(
        "AI-powered yoga pose detection "
        "and real-time posture correction."
    ),
    version="1.0.0",
)


# --------------------------------------------------
# CORS configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Initialize AI components
# --------------------------------------------------

pose_engine = PoseEngine()
analyzer = YogaAnalyzer()


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():
    """
    Basic API health check.
    """

    return {
        "message": "Yoga Motion AI API is running.",
        "status": "success",
    }


# --------------------------------------------------
# Health endpoint
# --------------------------------------------------

@app.get("/health")
def health_check():
    """
    Check whether the backend is healthy.
    """

    return {
        "status": "healthy",
        "service": "Yoga Motion AI",
    }


# --------------------------------------------------
# AI image analysis endpoint
# --------------------------------------------------

@app.post("/analyze-frame")
async def analyze_frame(
    file: UploadFile = File(...)
):
    """
    Receive one image frame and run the complete
    Yoga Motion AI analysis pipeline.

    Pipeline:

        Image
          ↓
        OpenCV
          ↓
        MediaPipe
          ↓
        33 landmarks
          ↓
        ML pose classifier
          ↓
        Posture analyzer
          ↓
        JSON response
    """

    # --------------------------------------------------
    # Read uploaded image
    # --------------------------------------------------

    image_bytes = await file.read()

    if not image_bytes:
        return {
            "status": "error",
            "message": "Empty image received.",
        }

    # --------------------------------------------------
    # Convert image bytes into NumPy array
    # --------------------------------------------------

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8,
    )

    # --------------------------------------------------
    # Decode image using OpenCV
    # --------------------------------------------------

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR,
    )

    if image is None:
        return {
            "status": "error",
            "message": "Could not decode the uploaded image.",
        }

    # --------------------------------------------------
    # Detect body pose using MediaPipe
    # --------------------------------------------------

    results = pose_engine.detect(image)

    landmarks = pose_engine.get_landmarks(
        results
    )

    # --------------------------------------------------
    # No body detected
    # --------------------------------------------------

    if landmarks is None:
        return {
            "status": "success",
            "pose": None,
            "confidence": 0.0,
            "posture": {
                "correct": False,
                "feedback": [
                    "No body detected."
                ],
            },
        }

    # --------------------------------------------------
    # Run ML + posture analysis
    # --------------------------------------------------

    analysis = analyzer.analyze(
        landmarks
    )

    # --------------------------------------------------
    # Return AI result
    # --------------------------------------------------

    return {
        "status": "success",
        "pose": analysis["pose"],
        "confidence": analysis["confidence"],
        "posture": analysis["posture"],
    }