import numpy as np
from django.shortcuts import render
from django.core.files.storage import default_storage
from keras.applications import MobileNetV3Small
from keras.applications.mobilenet_v3 import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array, load_img
from django.conf import settings
import os

# Load MobileNetV3Small model with pre-trained ImageNet weights
model = MobileNetV3Small(weights="imagenet")

def preprocess_image(image):
    # Convert image to array and expand dimensions for MobileNetV3Small
    image_array = img_to_array(image)
    expanded_image = np.expand_dims(image_array, axis=0)
    
    # Preprocess the image as required by MobileNetV3Small
    return preprocess_input(expanded_image.copy())

def home(request):
    if request.method == "POST":
        # Django image API
        file = request.FILES["imageFile"]
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)

        # Load and preprocess the image
        image = load_img(file_url, target_size=(224, 224))  # MobileNetV3Small expects 224x224 images
        processed_image = preprocess_image(image)

        # Predict using the MobileNetV3Small model
        predictions = model.predict(processed_image)

        # Decode predictions to get human-readable labels
        label = decode_predictions(predictions, top=5)[0]

        # Prepare image URL for rendering
        image_filename = os.path.basename(file_url)
        image_url = os.path.join(settings.MEDIA_URL, image_filename)

        # Render the result on the home page
        return render(request, "home.html", {"predictions": label, "image_url": image_url})
    
    else:
        return render(request, "home.html")
