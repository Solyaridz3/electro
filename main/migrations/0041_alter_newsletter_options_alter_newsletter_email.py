# Generated by Django 4.0.1 on 2022-02-14 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_newsletter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'verbose_name': 'Email', 'verbose_name_plural': 'Newsletter'},
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
