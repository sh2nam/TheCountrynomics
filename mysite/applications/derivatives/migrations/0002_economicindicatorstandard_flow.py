# Generated by Django 2.2.3 on 2019-10-24 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('derivatives', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='economicindicatorstandard',
            name='flow',
            field=models.CharField(default='NA', max_length=1),
            preserve_default=False,
        ),
    ]