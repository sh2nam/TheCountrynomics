# Generated by Django 2.2.3 on 2019-09-09 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EconomicIndicatorStandard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('dbcode', models.CharField(max_length=100)),
                ('indicator', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=20)),
                ('freq', models.CharField(max_length=10)),
                ('value', models.FloatField(default=None)),
                ('update_date', models.DateField(null=True)),
            ],
            options={
                'unique_together': {('date', 'dbcode', 'freq')},
            },
        ),
        migrations.CreateModel(
            name='EconomicIndicatorCounterparty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('dbcode', models.CharField(max_length=100)),
                ('indicator', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=20)),
                ('counter_party', models.CharField(max_length=20)),
                ('freq', models.CharField(max_length=10)),
                ('value', models.FloatField(default=None)),
                ('update_date', models.DateField(null=True)),
            ],
            options={
                'unique_together': {('date', 'dbcode', 'freq', 'counter_party')},
            },
        ),
    ]