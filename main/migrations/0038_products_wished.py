# Generated by Django 4.0.1 on 2022-02-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_alter_products_empty'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='wished',
            field=models.BooleanField(default=False, verbose_name='Wished'),
        ),
    ]
