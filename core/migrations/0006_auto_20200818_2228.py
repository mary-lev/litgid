# Generated by Django 3.1 on 2020-08-18 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200814_2148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['date'], 'verbose_name': 'Event'},
        ),
    ]
