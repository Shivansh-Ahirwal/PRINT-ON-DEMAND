# Generated by Django 5.1.4 on 2024-12-12 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_trending',
            field=models.BooleanField(default=False),
        ),
    ]
