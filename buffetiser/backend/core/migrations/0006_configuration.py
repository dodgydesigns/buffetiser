# Generated by Django 5.1.1 on 2025-02-01 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_investment_plot_path_alter_purchase_exchange_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Configuration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("update_time", models.CharField(default="15:00")),
                ("update_time_zone", models.CharField(default="Australia/Perth")),
            ],
        ),
    ]
