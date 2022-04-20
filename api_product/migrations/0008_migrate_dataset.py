# Generated by Django 3.2.8 on 2022-04-18 14:37
import uuid

from django.db import migrations
import  os


def init_data_category(apps, schema_editor):
    dataset_model = apps.get_model("api_product", "Dataset")
    category_model = apps.get_model("api_product", "Category")
    eraser_category = category_model.objects.filter(name="ERASER").first()
    note_category = category_model.objects.filter(name="STICKY NOTE").first()

    datasets = []

    valid_url = "api_product/constants/valid/"
    unvalid_url = "api_product/constants/unvalid/"
    logo = ['logo1', 'logo2']
    for i in range(len(logo)):
        url = valid_url + logo[i] + '.txt'
        f = open(url, "r")
        list = os.listdir(url)
        for j in range(len(list)):
            if i == 0:
                datasets.append(dataset_model(id=uuid.uuid4(), url=f.readline(), category=eraser_category))
            else:
                datasets.append(dataset_model(id=uuid.uuid4(), url=f.readline(), category=note_category))

    category_model.objects.bulk_create(datasets)

class Migration(migrations.Migration):

    dependencies = [
        ('api_product', '0007_dataset'),
    ]

    operations = [
    ]
