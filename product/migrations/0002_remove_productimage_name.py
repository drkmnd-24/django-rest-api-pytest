# Generated by Django 4.2.2 on 2023-06-20 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productimage",
            name="name",
        ),
    ]
