# Generated by Django 4.2.5 on 2023-09-22 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0009_alter_itemmodel_item_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemmodel',
            name='item_category',
        ),
    ]