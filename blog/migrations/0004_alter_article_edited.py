# Generated by Django 5.0.2 on 2024-03-15 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
