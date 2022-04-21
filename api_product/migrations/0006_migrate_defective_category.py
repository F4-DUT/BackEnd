from django.db import migrations
from api_product.constants import CategoryData


def init_data_category(apps, schema_editor):
    category_model = apps.get_model("api_product", "Category")

    categories = []
    category = CategoryData.DEFECTIVE_PRODUCT1
    category1 = CategoryData.DEFECTIVE_PRODUCT2
    categories.append(category_model(id=category.value['id'], name=category.value['name']))
    categories.append(category_model(id=category1.value['id'], name=category1.value['name']))

    category_model.objects.bulk_create(categories)


class Migration(migrations.Migration):

    dependencies = [
        ('api_product', '0005_migrate_product'),
    ]

    operations = [
        migrations.RunPython(init_data_category, migrations.RunPython.noop)
    ]
