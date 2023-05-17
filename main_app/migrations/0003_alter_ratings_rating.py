# Generated by Django 4.1.7 on 2023-04-10 07:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0002_alter_ratings_isbn_alter_ratings_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ratings",
            name="rating",
            field=models.IntegerField(
                default=0,
                validators=[
                    django.core.validators.MaxValueValidator(10),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
    ]
