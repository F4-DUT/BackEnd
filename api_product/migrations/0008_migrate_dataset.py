# Generated by Django 3.2.8 on 2022-04-18 14:37
import uuid

from django.db import migrations


def init_data_datasets(apps, schema_editor):
    dataset_model = apps.get_model("api_product", "Dataset")
    category_model = apps.get_model("api_product", "Category")
    eraser_category = category_model.objects.filter(name="ERASER").first()
    note_category = category_model.objects.filter(name="STICKY NOTE").first()
    eraser_defective = category_model.objects.filter(name="DEFECTIVE_ERASER").first()
    note_defective = category_model.objects.filter(name="DEFECTIVE_NOTE").first()

    datasets = []

    train_link = "api_product/constants/train_link/"
    logo = ['logo1', 'logo2']
    for i in range(len(logo)):
        url1 = train_link + logo[i] + '.txt'
        url2 = train_link + 'u' + logo[i] + '.txt'

        f = open(url1, "r")
        count = 0
        for line in open(url1):
            count += 1
        for j in range(count):
            if i == 0:
                datasets.append(dataset_model(id=uuid.uuid4(), url=f.readline(), category=eraser_category))
            else:
                datasets.append(dataset_model(id=uuid.uuid4(), url=f.readline(), category=note_category))

        f1 = open(url2, "r")
        count = 0
        for line in open(url2):
            count += 1
        for j in range(count):
            if i == 0:
                datasets.append(dataset_model(id=uuid.uuid4(), url=f1.readline(), category=eraser_defective))
            else:
                datasets.append(dataset_model(id=uuid.uuid4(), url=f1.readline(), category=note_defective))

    dataset_model.objects.bulk_create(datasets)


def delete_all_data(apps, schema_editor):
    dataset_model = apps.get_model("api_product", "Dataset")
    dataset_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api_product', '0007_dataset'),
    ]

    operations = [
        migrations.RunPython(init_data_datasets, delete_all_data)
    ]
