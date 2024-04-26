# Generated by Django 3.2.12 on 2024-04-16 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0006_auto_20240416_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomcategory',
            old_name='room_image',
            new_name='image_de_la_salle',
        ),
        migrations.AlterField(
            model_name='roomcategory',
            name='motif_de_reservation',
            field=models.CharField(default='', max_length=50),
        ),
    ]