import tensorflow as tf
import os
import numpy as np
from keras.preprocessing import image
from api_product.models import Category


class CategoryService:
    @classmethod
    def check_category(cls, image1):
        from PIL import Image as pil
        img = pil.open(image1).resize((150, 150))
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
        saved_model = tf.keras.models.load_model("api_product/constants/eraser_data.h5")
        x = image.img_to_array(img) / 255
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])
        classes = saved_model.predict(images, batch_size=10)

        if classes[0] > 0.5:
            return Category.objects.filter(name="STICKY NOTE").first()
        else:
            return Category.objects.filter(name="ERASER").first()
