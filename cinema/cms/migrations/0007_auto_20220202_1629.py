# Generated by Django 3.2 on 2022-02-02 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20220202_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='image_ru',
        ),
        migrations.RemoveField(
            model_name='page',
            name='image_uk',
        ),
    ]