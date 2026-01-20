from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from pathlib import Path



def predict_with_model(img):
    trained_classes = {"Angry": 0, "Fear": 1, "Happy": 2, "Sad": 3, "Surprise": 4}

    BASE_DIR = Path(__file__).resolve().parent.parent
    model_path = BASE_DIR / "Model" / "emotional_model.h5"

    resized_img = resize(img, (150, 150))
    final_shaped_img = resized_img[np.newaxis, ...]

    my_model = load_model(model_path)
    predictions = my_model.predict(final_shaped_img)
    index = np.argmax(predictions[0])
    for key, value in trained_classes.items():
        if value == index:
            return key