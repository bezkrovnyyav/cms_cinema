# Generated by Django 3.2 on 2022-03-18 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0028_auto_20220318_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='date',
            field=models.DateField(null=True),
        ),
    ]