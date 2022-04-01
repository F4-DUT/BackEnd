from enum import Enum


class RoleData(Enum):
    ADMIN = {
        "id": "aef45b7b6f9745428594caa9ed3ec5f8",
        "name": "ADMIN"
    }

    MANAGER = {
        "id":  "91a0e81fd2064dd182669d4dd592d209",
        "name": "MANAGER"
    }

    EMPLOYEE = {
        "id": "af63504a122c406f9fd9f3b7162b7591",
        "name": "EMPLOYEE"
    }

    RASPBERRY = {
        "id": "a186c1d79fca4370964aa27a778ec989",
        "name": "RASPBERRY"
    }


class UserData:
    employees = [
        {
            "id": 2,
            "email": "giabao2807@gmail.com",
            "first_name": "Bảo",
            "last_name": "Gia",
            "address": "Điện Phước, Điện Bàn, Quảng Nam",
            "phone": "0915181914",
            "age": 20
        },
        {
            "id": 3,
            "email": "nguyen13901@gmail.com",
            "first_name": "Nguyên",
            "last_name": "Thành",
            "address": "Điện Phương, Điện Bàn, Quảng Nam",
            "phone": "0944194927",
            "age": 20
        },
        {
            "id": 4,
            "email": "thienho549@gmail.com",
            "first_name": "Thiện",
            "last_name": "Hoàng",
            "address": "Thăng Bình, Quảng Nam",
            "phone": "0334298720",
            "age": 20
        },
        {
            "id": 5,
            "email": "trancongviet0710@gmail.com",
            "first_name": "Việt",
            "last_name": "Công",
            "address": "Điện Phước, Điện Bàn, Quảng Nam",
            "phone": "0935169835",
            "age": 20
        }
    ]
    managers = [
        {
            "id": 6,
            "email": "bttthanh@dut.udn.vn",
            "first_name": "Thanh",
            "last_name": "Thanh",
            "address": "Đà Nẵng",
            "phone": "0961055111",
            "age": 30
        }
    ]
