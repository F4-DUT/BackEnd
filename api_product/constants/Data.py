from enum import Enum
import uuid


class CategoryData(Enum):
    ERASER = {
        "id": "fb974149511d48859c6bcff2d54483ed",
        "name": "ERASER"
    }

    NOTE = {
        "id": "308cd8f9ce044a308f0dc858e86f671c",
        "name": "STICKY NOTE"
    }

    DEFECTIVE_PRODUCT1 = {
        "id": "c44410dcfe9e4aa89f4f821e51b956d5",
        "name": "DEFECTIVE_ERASER"
    }

    DEFECTIVE_PRODUCT2 = {
        "id": "bfbf186c983848fb89d59bef10882366",
        "name": "DEFECTIVE_NOTE"
    }

class ProductData:
    erasers = [
        {
            "id": uuid.uuid4(),
            "name": "eraser product 01"
        },
        {
            "id": uuid.uuid4(),
            "name": "eraser product 02"
        },
        {
            "id": uuid.uuid4(),
            "name": "eraser product 03"
        },
        {
            "id": uuid.uuid4(),
            "name": "eraser product 04"
        },
        {
            "id": uuid.uuid4(),
            "name": "eraser product 05"
        }
    ]

    notes = [
        {
            "id": uuid.uuid4(),
            "name": "sticky note 01"
        },
        {
            "id": uuid.uuid4(),
            "name": "sticky note 02"
        },
        {
            "id": uuid.uuid4(),
            "name": "sticky note 03"
        },
        {
            "id": uuid.uuid4(),
            "name": "sticky note 04"
        },
        {
            "id": uuid.uuid4(),
            "name": "sticky note 05"
        }
    ]
