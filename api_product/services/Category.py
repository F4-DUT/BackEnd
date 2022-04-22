import tensorflow as tf
import numpy as np
import cv2
from api_product.models import Category


class CategoryService:
    @classmethod
    def check_category(cls, image1):
        from PIL import Image as pil
        saved_model = tf.keras.models.load_model("api_product/constants/classify_model.h5")
        pil_img = pil.open(image1).resize((150, 150)).convert('RGB')
        img_arr = np.array(pil_img)
        # Convert RGB to BGR
        img_arr = img_arr[:, :, ::-1].copy()
        img_arr = cv2.resize(img_arr, (150, 150))
        x = img_arr.astype("float") / 255.0

        x = np.expand_dims(x, axis=0)
        classes = saved_model.predict(x)
        category_num = np.argmax(classes)

        if category_num == 1:
            return Category.objects.filter(name="STICKY NOTE").first()
        elif category_num == 0:
            return Category.objects.filter(name="ERASER").first()
        elif category_num == 2:
            return Category.objects.filter(name="DEFECTIVE_ERASER").first()
        else:
            return Category.objects.filter(name="DEFECTIVE_NOTE").first()

