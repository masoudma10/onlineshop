# Generated by Django 3.2 on 2021-05-06 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(max_length=555, unique=True),
        ),
    ]
