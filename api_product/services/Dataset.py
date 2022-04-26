import uuid

import cloudinary
import cloudinary.api
import cloudinary.uploader

import os
from dotenv import load_dotenv

from api_product.constants import CategoryData
from api_product.models import Dataset

load_dotenv()


class DatasetService:
    @classmethod
    def upload_images(cls, images, category):
        images_urls = []
        category_map = ['logo1', 'logo2', 'unvalid1', 'unvalid2']

        if category.name == CategoryData.NOTE.value.get('name'):
            folder_url = os.getenv('CLOUDINARY_DATASET_FOLDER') + category_map[1]
        if category.name == CategoryData.ERASER.value.get('name'):
            folder_url = os.getenv('CLOUDINARY_DATASET_FOLDER') + category_map[0]
        if category.name == CategoryData.DEFECTIVE_PRODUCT1.value.get('name'):
            folder_url = os.getenv('CLOUDINARY_DATASET_FOLDER') + category_map[2]
        if category.name == CategoryData.DEFECTIVE_PRODUCT2.value.get('name'):
            folder_url = os.getenv('CLOUDINARY_DATASET_FOLDER') + category_map[3]
        for image in images:
            upload_image = cloudinary.uploader.upload(image, folder=folder_url)
            images_urls.append(upload_image.get('url'))
        return images_urls

    @classmethod
    def create(cls, image_urls, category):
        datasets = []

        for url in image_urls:
            datasets.append(Dataset(id=uuid.uuid4(), url=url, category=category))

        Dataset.objects.bulk_create(datasets)
        return datasets
