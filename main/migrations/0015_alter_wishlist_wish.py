# Generated by Django 4.0.1 on 2022-02-04 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_products_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='wish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products'),
        ),
    ]
