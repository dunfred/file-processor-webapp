# Generated by Django 2.2 on 2019-09-24 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output', models.FileField(upload_to='documents/%Y/%m/%d/Final Output/')),
            ],
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='documents/%Y/%m/%d/Raw Data/'),
        ),
    ]
