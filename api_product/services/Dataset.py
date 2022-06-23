import uuid

import cloudinary
import cloudinary.api
import cloudinary.uploader

import os
from dotenv import load_dotenv

from api_product.constants import CategoryData
from api_product.models import Dataset

import requests
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import random
import numpy as np
import pickle

from imutils import paths
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import SGD
from keras.preprocessing import image
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer

load_dotenv()


class DatasetService:
    @classmethod
    def upload_images(cls, images, category):
        images_urls = []
        category_map = ['logo1', 'logo2', 'ulogo1', 'ulogo2']

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

    @classmethod
    def train(cls):
        try:
            TRAIN_LINK = "api_product/constants/train_link/"
            VALID_LINK = "api_product/constants/valid_link/"
            TRAIN = "api_product/constants/train/"
            VALID = "api_product/constants/valid/"

            logo1 = "logo1"
            logo2 = "logo2"
            ulogo1 = "ulogo1"
            ulogo2 = "ulogo2"

            TRAIN_DIRS = [TRAIN_LINK + logo1 + ".txt", TRAIN_LINK + logo2 + ".txt", TRAIN_LINK + ulogo1 + ".txt",
                          TRAIN_LINK + ulogo2 + ".txt"]
            VALID_DIRS = [VALID_LINK + logo1 + ".txt", VALID_LINK + logo2 + ".txt", VALID_LINK + ulogo1 + ".txt",
                          VALID_LINK + ulogo2 + ".txt"]
            DIRS = [TRAIN_DIRS, VALID_DIRS]

            TRAIN_DATA = [TRAIN + logo1 + "/", TRAIN + logo2 + "/", TRAIN + ulogo1 + "/", TRAIN + ulogo2 + "/"]
            VALID_DATA = [VALID + logo1 + "/", VALID + logo2 + "/", VALID + ulogo1 + "/", VALID + ulogo2 + "/"]
            DATA = [TRAIN_DATA, VALID_DATA]

            # for l in range(2):
            #     for i in range(4):
            #         ## read links url
            #         with open(DIRS[l][i], 'r') as f:
            #             links = f.readlines()
            #             print(links)
            #
            #         ## download images from links
            #         for j in range(len(links)):
            #             response = requests.get(links[j])
            #             file = open(DATA[l][i] + str(j) + ".png", "wb")
            #             file.write(response.content)
            #             file.close()

                        ## Build file .pkl
            TRAIN_DIRECTORY = "api_product/constants/train"
            VALID_DIRECTORY = "api_product/constants/valid"
            DIRECTORY = [TRAIN_DIRECTORY, VALID_DIRECTORY]
            CATEGORIES = ['logo1', 'logo2', 'ulogo1', 'ulogo2']

            IMG_SIZE = 150

            train_data = []
            valid_data = []
            data = [train_data, valid_data]


            for i in range(2):
                for category in CATEGORIES:
                    folder = os.path.join(DIRECTORY[i], category)
                    label = CATEGORIES.index(category)
                    for img in os.listdir(folder):
                        img_path = os.path.join(folder, img)
                        img_arr = cv2.imread(img_path)
                        img_arr = cv2.resize(img_arr, (IMG_SIZE, IMG_SIZE))
                        data[i].append([img_arr, label])

            random.shuffle(data[0])
            random.shuffle(data[1])

            train_x = []
            train_y = []
            valid_x = []
            valid_y = []
            x = [train_x, valid_x]
            y = [train_y, valid_y]

            for i in range(2):
                for features, labels in data[i]:
                    x[i].append(features)
                    y[i].append(labels)

            TRAIN_X = np.array(x[0])
            TRAIN_Y = np.array(y[0])
            VALID_X = np.array(x[1])
            VALID_Y = np.array(y[1])

            pickle.dump(TRAIN_X, open('api_product/constants/train_features.pkl', 'wb'))
            pickle.dump(TRAIN_Y, open('api_product/constants/train_labels.pkl', 'wb'))
            pickle.dump(VALID_X, open('api_product/constants/valid_features.pkl', 'wb'))
            pickle.dump(VALID_Y, open('api_product/constants/valid_labels.pkl', 'wb'))

            # ## build model

            trainX = pickle.load(open('api_product/constants/train_features.pkl', 'rb'))
            trainY = pickle.load(open('api_product/constants/train_labels.pkl', 'rb'))

            validX = pickle.load(open('api_product/constants/valid_features.pkl', 'rb'))
            validY = pickle.load(open('api_product/constants/valid_labels.pkl', 'rb'))

            # Build model
            model = Sequential()

            model.add(Conv2D(32, (3, 3), padding="same", activation="relu", input_shape=(150, 150, 3)))
            model.add(BatchNormalization(axis=-1))
            model.add(Conv2D(32, (3, 3), padding="same", activation="relu"))
            model.add(BatchNormalization(axis=-1))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.25))

            model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
            model.add(BatchNormalization(axis=-1))
            model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
            model.add(BatchNormalization(axis=-1))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.25))

            model.add(Flatten())
            model.add(Dense(512, activation="relu"))
            model.add(BatchNormalization())
            model.add(Dropout(0.5))
            model.add(Dense(4, activation="softmax"))

            # model.summary()

            opt = SGD(learning_rate=0.0001, momentum=0.9)

            model.compile(
                optimizer=opt,
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )

            aug = ImageDataGenerator(
                rotation_range=0.1,
                zoom_range=0.1,
                width_shift_range=0.2,
                height_shift_range=0.2,
                horizontal_flip=True)

            trainX = trainX.astype("float") / 255.0
            validX = validX.astype("float") / 255.0

            from sklearn.preprocessing import LabelBinarizer

            lb = LabelBinarizer()

            trainY = lb.fit_transform(trainY)
            validY = lb.fit_transform(validY)

            H = model.fit_generator(
                aug.flow(trainX, trainY, batch_size=30),
                validation_data=(validX, validY),
                steps_per_epoch=trainX.shape[0] // 30,
                epochs=6, verbose=1)

            model.save("api_product/constants/classify_model.h5")
            return True
        except Exception as e:
            print(str(e))
            return False