import numpy as np
from django.shortcuts import render
from django.core.files.storage import default_storage
from keras.applications import vgg16
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array, load_img
from django.conf import settings
import os

model = vgg16.VGG16(weights="imagenet")

def preprocess_image(image):
    image_array = img_to_array(image)
    expanded_image = np.expand_dims(image_array, axis=0)
    return vgg16.preprocess_input(expanded_image.copy())

def home(request):
    if request.method == "POST":
        # Django image API
        file = request.FILES["imageFile"]
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)
        image = load_img(file_url, target_size=(224, 224))
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        label = decode_predictions(predictions,top=5)[0]
        image_filename = os.path.basename(file_url)
        image_url = os.path.join(settings.MEDIA_URL, image_filename)
        return render(request, "home.html", {"predictions": label, "image_url": image_url})
    else:
        return render(request, "home.html")
