# Generated by Django 3.2.12 on 2024-05-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0010_auto_20240503_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomcategory',
            name='image',
            field=models.ImageField(default='default_image/default.jpg', upload_to='default_image'),
        ),
    ]