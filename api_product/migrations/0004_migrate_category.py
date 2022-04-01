from django.db import migrations

from api_product.constants import CategoryData


def init_data_category(apps, schema_editor):
    category_model = apps.get_model("api_product", "Category")

    categories = []
    for category in CategoryData:
        categories.append(category_model(id=category.value['id'], name=category.value['name']))

    category_model.objects.bulk_create(categories)


def delete_all_data(apps, schema_editor):
    category_model = apps.get_model("api_product", "Category")
    category_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api_product', '0003_alter_product_options'),
    ]

    operations = [
        migrations.RunPython(init_data_category, delete_all_data)
    ]
