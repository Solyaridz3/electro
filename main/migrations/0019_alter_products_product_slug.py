# Generated by Django 4.0.1 on 2022-02-04 12:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_products_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_slug',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
