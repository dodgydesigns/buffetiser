# Generated by Django 5.1.1 on 2024-10-04 23:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Financials",
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
                ("total_value", models.FloatField()),
                ("total_spent_on_purchase", models.FloatField()),
                ("total_earned_on_sale", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Investment",
            fields=[
                (
                    "key",
                    models.CharField(
                        default=None, max_length=32, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(default=None, max_length=128, null=True)),
                ("symbol", models.CharField(default=None, max_length=32, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("Shares", "Shares"), ("Crypto", "Crypto")],
                        default="Shares",
                        max_length=16,
                    ),
                ),
                ("live_price", models.FloatField(default=0)),
                ("plot_path", models.CharField(default="./", max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name="History",
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
                ("date", models.DateField()),
                ("high", models.FloatField(default=0)),
                ("low", models.FloatField(default=0)),
                ("close", models.FloatField(default=0)),
                ("volume", models.IntegerField(default=0)),
                (
                    "investment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.investment",
                    ),
                ),
            ],
            options={
                "unique_together": {("date", "investment")},
            },
        ),
        migrations.CreateModel(
            name="DividendReinvestment",
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
                ("reinvestment_date", models.DateField()),
                ("units", models.IntegerField(default=0)),
                (
                    "investment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.investment",
                    ),
                ),
            ],
            options={
                "unique_together": {("reinvestment_date", "investment")},
            },
        ),
        migrations.CreateModel(
            name="DividendPayment",
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
                ("payment_date", models.DateField()),
                ("value", models.FloatField()),
                (
                    "investment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.investment",
                    ),
                ),
            ],
            options={
                "unique_together": {("payment_date", "investment")},
            },
        ),
        migrations.CreateModel(
            name="Purchase",
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
                ("currency", models.CharField(default="AUD", max_length=5)),
                (
                    "exchange",
                    models.CharField(
                        choices=[
                            ("XAMS", "XAMS"),
                            ("XASX", "XASX"),
                            ("XBOM", "XBOM"),
                            ("XBRU", "XBRU"),
                            ("XFRA", "XFRA"),
                            ("XHKG", "XHKG"),
                            ("XJPX", "XJPX"),
                            ("XKOS", "XKOS"),
                            ("XLIS", "XLIS"),
                            ("XLON", "XLON"),
                            ("XMIL", "XMIL"),
                            ("XMSM", "XMSM"),
                            ("XNAS", "XNAS"),
                            ("XNSE", "XNSE"),
                            ("XNYS", "XNYS"),
                            ("XOSL", "XOSL"),
                            ("XSAU", "XSAU"),
                            ("XSHE", "XSHE"),
                            ("XSHG", "XSHG"),
                            ("XSWX", "XSWX"),
                            ("XTAI", "XTAI"),
                            ("XTSE", "XTSE"),
                        ],
                        default="XASX",
                        max_length=4,
                    ),
                ),
                (
                    "platform",
                    models.CharField(
                        choices=[
                            ("CMC", "CMC"),
                            ("LINK", "LINK"),
                            ("BOARDROOM", "BOARDROOM"),
                            ("DIRECT", "DIRECT"),
                            ("IPO", "IPO"),
                        ],
                        default="CMC",
                        max_length=128,
                    ),
                ),
                ("units", models.FloatField()),
                ("price_per_unit", models.FloatField()),
                ("fee", models.FloatField()),
                ("date", models.DateField()),
                ("trade_count", models.IntegerField()),
                (
                    "investment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.investment",
                    ),
                ),
            ],
            options={
                "unique_together": {("date", "trade_count", "investment")},
            },
        ),
        migrations.CreateModel(
            name="Sale",
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
                ("currency", models.CharField(default="AUD", max_length=5)),
                (
                    "exchange",
                    models.CharField(
                        choices=[
                            ("XAMS", "XAMS"),
                            ("XASX", "XASX"),
                            ("XBOM", "XBOM"),
                            ("XBRU", "XBRU"),
                            ("XFRA", "XFRA"),
                            ("XHKG", "XHKG"),
                            ("XJPX", "XJPX"),
                            ("XKOS", "XKOS"),
                            ("XLIS", "XLIS"),
                            ("XLON", "XLON"),
                            ("XMIL", "XMIL"),
                            ("XMSM", "XMSM"),
                            ("XNAS", "XNAS"),
                            ("XNSE", "XNSE"),
                            ("XNYS", "XNYS"),
                            ("XOSL", "XOSL"),
                            ("XSAU", "XSAU"),
                            ("XSHE", "XSHE"),
                            ("XSHG", "XSHG"),
                            ("XSWX", "XSWX"),
                            ("XTAI", "XTAI"),
                            ("XTSE", "XTSE"),
                        ],
                        default="XASX",
                        max_length=4,
                    ),
                ),
                ("units", models.FloatField()),
                ("price_per_unit", models.FloatField()),
                ("fee", models.FloatField()),
                ("date", models.DateField()),
                ("trade_count", models.IntegerField()),
                (
                    "investment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.investment",
                    ),
                ),
            ],
            options={
                "unique_together": {("date", "trade_count", "investment")},
            },
        ),
    ]
