import os

from django.contrib.auth.hashers import make_password
from django.db import migrations

from api_account.constants import UserData


def initial_user_data(apps, schema_editor):
    account_model = apps.get_model("api_account", "Account")
    role_model = apps.get_model("api_account", "Role")
    employee_role = role_model.objects.filter(name="EMPLOYEE").first()
    manager_role = role_model.objects.filter(name="MANAGER").first()

    accounts = []

    for employee in UserData.employees:
        accounts.append(account_model(is_superuser=False, id=employee['id'], first_name=employee['first_name'],
                                      last_name=employee['last_name'],
                                      is_staff=True,
                                      username=employee['email'].split('@')[0],
                                      avatar=employee.get('avatar', 'https://res.cloudinary.com/boninguci/image/upload/v1647265302/pbl5/avatar/nam_qnitkh.png'),
                                      email=employee['email'], address=employee['address'],
                                      phone=employee['phone'],
                                      age=employee['age'],
                                      password=make_password(os.getenv('DEFAULT_EMPLOYEE_PASSWORD')),
                                      role=employee_role))

    for manager in UserData.managers:
        accounts.append(account_model(is_superuser=True, id=manager['id'], first_name=manager['first_name'],
                                      last_name=manager['last_name'],
                                      is_staff=True,
                                      username=manager['email'].split('@')[0],
                                      avatar=manager.get('avatar', 'https://res.cloudinary.com/boninguci/image/upload/v1647265302/pbl5/avatar/nam_qnitkh.png'),
                                      email=manager['email'], address=manager['address'],
                                      phone=manager['phone'],
                                      age=manager['age'],
                                      password=make_password(os.getenv('DEFAULT_MANAGER_PASSWORD')),
                                      role=manager_role))

    account_model.objects.bulk_create(accounts)


def delete_all_data(apps, schema_editor):
    account_model = apps.get_model("api_account", "Account")
    account_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api_account', '0005_migrate_admin'),
    ]

    operations = [
        migrations.RunPython(initial_user_data, delete_all_data)
    ]
