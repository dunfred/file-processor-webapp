# Generated by Django 2.2 on 2019-09-24 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20190924_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='documents/Raw Data/'),
        ),
        migrations.AlterField(
            model_name='new_document',
            name='docfile',
            field=models.FileField(upload_to='documents/Final Output/'),
        ),
    ]
