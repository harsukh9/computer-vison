from fastapi import FastAPI, File, UploadFile, HTTPException
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io

# Create the FastAPI app
app = FastAPI()

# Load the model
model = load_model("models/cifar10_cnn_model.h5")

# Class names for CIFAR-10
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Preprocess function
def preprocess_image(image):
    image = image.resize((32, 32))  # Resize image to 32x32
    image = np.array(image) / 255.0  # Normalize pixel values
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the CIFAR-10 Image Classification API!"}

# Prediction endpoint
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JPEG or PNG image.")

    # Read and preprocess the image
    image = Image.open(io.BytesIO(await file.read()))
    image = preprocess_image(image)

    # Make prediction
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction, axis=1)[0]
    confidence = float(np.max(prediction))

    return {
        "predicted_class": class_names[predicted_class],
        "confidence": confidence
    }
