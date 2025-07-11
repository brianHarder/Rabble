# Generated by Django 5.1.7 on 2025-05-11 22:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rabble", "0010_anonymous_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="subrabble",
            name="user_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
