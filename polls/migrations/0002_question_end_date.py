# Generated by Django 4.1.1 on 2022-09-09 13:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="end_date",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="end_date"),
            preserve_default=False,
        ),
    ]