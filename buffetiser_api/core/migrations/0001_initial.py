# Generated by Django 4.2.6 on 2023-10-06 01:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('symbol', models.CharField(max_length=32)),
                ('investment_type', models.CharField(choices=[('Shares', 'Shares'), ('Crypto', 'Crypto')], default='Shares', max_length=16)),
                ('live_price', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.IntegerField()),
                ('price_per_unit', models.IntegerField()),
                ('fees', models.IntegerField()),
                ('date_time', models.DateField(default=django.utils.timezone.now)),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='core.investment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('CMC', 'CMC'), ('LINK', 'LINK'), ('BOARDROOM', 'BOARDROOM'), ('DIRECT', 'DIRECT'), ('IPO', 'IPO')], default='CMC', max_length=128)),
                ('currency', models.CharField(default='AUD', max_length=5)),
                ('exchange', models.CharField(choices=[('XAMS', 'XAMS'), ('XASX', 'XASX'), ('XBOM', 'XBOM'), ('XBRU', 'XBRU'), ('XFRA', 'XFRA'), ('XHKG', 'XHKG'), ('XJPX', 'XJPX'), ('XKOS', 'XKOS'), ('XLIS', 'XLIS'), ('XLON', 'XLON'), ('XMIL', 'XMIL'), ('XMSM', 'XMSM'), ('XNAS', 'XNAS'), ('XNSE', 'XNSE'), ('XNYS', 'XNYS'), ('XOSL', 'XOSL'), ('XSAU', 'XSAU'), ('XSHE', 'XSHE'), ('XSHG', 'XSHG'), ('XSWX', 'XSWX'), ('XTAI', 'XTAI'), ('XTSE', 'XTSE')], default='XASX', max_length=4)),
                ('units', models.IntegerField()),
                ('fees', models.IntegerField()),
                ('price_per_unit', models.IntegerField()),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='core.investment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('open', models.IntegerField(default=0)),
                ('high', models.IntegerField(default=0)),
                ('low', models.IntegerField(default=0)),
                ('close', models.IntegerField(default=0)),
                ('volume', models.IntegerField(default=0)),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.investment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
