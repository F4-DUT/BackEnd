from django.db import migrations
from api_product.constants import CategoryData


def init_data_category(apps, schema_editor):
    category_model = apps.get_model("api_product", "Category")

    categories = []
    category = CategoryData.DEFECTIVE_PRODUCT1
    categories.append(category_model(id=category.value['id'], name=category.value['name']))

    category_model.objects.bulk_create(categories)


class Migration(migrations.Migration):

    dependencies = [
        ('api_product', '0005_migrate_product'),
    ]

    operations = [
        migrations.RunPython(init_data_category, migrations.RunPython.noop)
    ]
