# Generated by Django 5.0.2 on 2024-03-14 21:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productId', models.PositiveIntegerField()),
                ('userId', models.PositiveIntegerField()),
                ('state', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SuggestionInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestionId', models.PositiveIntegerField()),
                ('field', models.TextField()),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SuggestionNutriment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestionId', models.PositiveIntegerField()),
                ('nutrimentId', models.PositiveIntegerField()),
                ('value', models.PositiveIntegerField()),
            ],
        ),
    ]
