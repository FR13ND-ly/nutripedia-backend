# Generated by Django 5.0.2 on 2024-03-16 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_rename_quantityunit_product_weight_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='origins',
        ),
    ]
