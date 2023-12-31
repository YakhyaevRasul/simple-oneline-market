# Generated by Django 3.2.8 on 2022-02-08 12:04

from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_product_is_famous'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='photo',
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(default='media/default-photo.jpg', upload_to=product.models.product_image_file_path)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
        ),
    ]
