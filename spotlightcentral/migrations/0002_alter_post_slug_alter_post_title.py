# Generated by Django 5.1.4 on 2024-12-30 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotlightcentral', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=250, unique_for_date='publish'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
