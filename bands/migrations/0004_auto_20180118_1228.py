# Generated by Django 2.0 on 2018-01-18 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0003_product_ad_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image_path',
            field=models.ImageField(upload_to='static/product_images/'),
        ),
        migrations.AlterField(
            model_name='product_ad',
            name='cover_image',
            field=models.ImageField(upload_to='static/product_cover_image/'),
        ),
    ]