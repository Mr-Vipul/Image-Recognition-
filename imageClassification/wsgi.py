"""
WSGI config for imageClassification project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import tensorflow as tf

from django.core.wsgi import get_wsgi_application

# TensorFlow configuration to manage memory
def configure_tensorflow():
    # Set TensorFlow to use only CPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    # Configure TensorFlow to limit GPU memory usage if a GPU is available
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(f"TensorFlow memory configuration error: {e}")

# Apply TensorFlow configuration
configure_tensorflow()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imageClassification.settings")

application = get_wsgi_application()
