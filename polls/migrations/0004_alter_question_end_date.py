# Generated by Django 4.1.1 on 2022-09-18 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0003_remove_choice_votes_vote"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="end_date",
            field=models.DateTimeField(verbose_name="end_date"),
        ),
    ]