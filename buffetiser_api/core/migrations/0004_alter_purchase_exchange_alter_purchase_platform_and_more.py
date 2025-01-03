# Generated by Django 5.1.1 on 2024-12-14 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_dailychange"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchase",
            name="exchange",
            field=models.CharField(
                choices=[
                    ("AMS", "Xams"),
                    ("ASX", "Xasx"),
                    ("BOM", "Xbom"),
                    ("BRU", "Xbru"),
                    ("FRA", "Xfra"),
                    ("HKG", "Xhkg"),
                    ("JPX", "Xjpx"),
                    ("KOS", "Xkos"),
                    ("LIS", "Xlis"),
                    ("LON", "Xlon"),
                    ("MIL", "Xmil"),
                    ("MSM", "Xmsm"),
                    ("NAS", "Xnas"),
                    ("NSE", "Xnse"),
                    ("NYS", "Xnys"),
                    ("OSL", "Xosl"),
                    ("SAU", "Xsau"),
                    ("SHE", "Xshe"),
                    ("SHG", "Xshg"),
                    ("SWX", "Xswx"),
                    ("TAI", "Xtai"),
                    ("TSE", "Xtse"),
                ],
                default="ASX",
                max_length=4,
            ),
        ),
        migrations.AlterField(
            model_name="purchase",
            name="platform",
            field=models.CharField(
                choices=[
                    ("CMC", "Cmc"),
                    ("LINK", "Link"),
                    ("BOARDROOM", "Boardroom"),
                    ("DIRECT", "Direct"),
                    ("IPO", "Ipo"),
                ],
                default="CMC",
                max_length=128,
            ),
        ),
        migrations.AlterField(
            model_name="sale",
            name="exchange",
            field=models.CharField(
                choices=[
                    ("AMS", "Xams"),
                    ("ASX", "Xasx"),
                    ("BOM", "Xbom"),
                    ("BRU", "Xbru"),
                    ("FRA", "Xfra"),
                    ("HKG", "Xhkg"),
                    ("JPX", "Xjpx"),
                    ("KOS", "Xkos"),
                    ("LIS", "Xlis"),
                    ("LON", "Xlon"),
                    ("MIL", "Xmil"),
                    ("MSM", "Xmsm"),
                    ("NAS", "Xnas"),
                    ("NSE", "Xnse"),
                    ("NYS", "Xnys"),
                    ("OSL", "Xosl"),
                    ("SAU", "Xsau"),
                    ("SHE", "Xshe"),
                    ("SHG", "Xshg"),
                    ("SWX", "Xswx"),
                    ("TAI", "Xtai"),
                    ("TSE", "Xtse"),
                ],
                default="ASX",
                max_length=4,
            ),
        ),
    ]
