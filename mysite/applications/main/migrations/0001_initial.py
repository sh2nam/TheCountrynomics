# Generated by Django 2.2.3 on 2019-09-09 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=264)),
                ('message', models.CharField(max_length=1000)),
                ('date', models.DateField()),
            ],
        ),
    ]
