# Generated by Django 5.1.7 on 2025-06-04 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rabble", "0014_rabble_description_rabble_private"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(default="images/default.png", upload_to="images/"),
        ),
    ]
