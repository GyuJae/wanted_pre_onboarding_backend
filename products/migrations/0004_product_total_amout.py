# Generated by Django 3.2.12 on 2022-04-05 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20220405_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_amout',
            field=models.IntegerField(default=0),
        ),
    ]
