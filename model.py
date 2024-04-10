import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

IMAGE_RES = 100

class MLModel:
    def __init__(self, model_path='model_weights.weights.h5'):
        """
        Initialize the ML model by loading the trained weights.
        :param model_path: Path to the saved model weights.
        """
        self.model_path = model_path
        self.model = load_model(model_path)
    def create_model(model_path='model_weights.weights.h5'):
        return MLModel(model_path)
    
    def predict_from_path(self, img_path):
        """
        Predict the class of an image using its file path.
        :param img_path: Path to the image file.
        :return: Predicted class.
        """
        img = image.load_img(img_path, target_size=(IMAGE_RES, IMAGE_RES))
        return self.predict(img)

    def predict_from_image(self, img):
        """
        Predict the class of an image using a PIL.Image object.
        :param img: A PIL.Image object of the image.
        :return: Predicted class.
        """
        if img.size != (IMAGE_RES, IMAGE_RES):
            img = img.resize((IMAGE_RES, IMAGE_RES))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)
        return predicted_class

    def update_model(self, new_model_path):
        """
        Update the model by loading a new set of weights.
        :param new_model_path: Path to the new model weights.
        """
        self.model_path = new_model_path
        self.model = load_model(new_model_path)
