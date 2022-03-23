from enum import Enum
import uuid


class CategoryData(Enum):
    ERASER = {
        "id": "fb974149-511d-4885-9c6b-cff2d54483ed",
        "name": "ERASER"
    }

    NOTE = {
        "id": "308cd8f9-ce04-4a30-8f0d-c858e86f671c",
        "name": "STICKY NOTE"
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
