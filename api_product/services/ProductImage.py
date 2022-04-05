from api_product.models import ProductImage
import cloudinary
import cloudinary.api
import cloudinary.uploader

import os
from dotenv import load_dotenv

load_dotenv()


class ProductImageService:
    @classmethod
    def upload_image(cls, image):
        upload_image = cloudinary.uploader.upload(image, folder=os.getenv('CLOUDINARY_PRODUCT_FOLDER'))
        return upload_image.get('url')

    @classmethod
    def upload_images(cls, images):
        images_url = []
        for image in images:
            upload_image = cloudinary.uploader.upload(image, folder=os.getenv('CLOUDINARY_PRODUCT_FOLDER'))
            images_url.append(upload_image.get('url'))
        return images_url

    @classmethod
    def create(cls, image_url, product):
        product_image = ProductImage(image=image_url, product=product)
        product_image.save()
        return product_image

    @classmethod
    def create(cls, image_urls, product):
        for image_url in image_urls:
            product_image = ProductImage(image=image_url, product=product)
            product_image.save()
