# Generated by Django 4.0 on 2022-01-09 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_productcomment_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productcomment',
            unique_together=set(),
        ),
    ]
