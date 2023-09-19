# Generated by Django 4.1.3 on 2022-11-06 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('adjustedClose', models.FloatField()),
                ('volume', models.IntegerField()),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.investment')),
            ],
        ),
    ]
