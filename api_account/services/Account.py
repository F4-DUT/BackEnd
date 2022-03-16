import cloudinary
import cloudinary.api
import cloudinary.uploader

import os
from dotenv import load_dotenv

load_dotenv()


class AccountService:
    @classmethod
    def upload_avatar(cls, avatar):
        upload_avatar = cloudinary.uploader.upload(avatar, folder=os.getenv('CLOUDINARY_AVATAR_USER_FOLDER'))
        return upload_avatar.get('url')
