# Generated by Django 3.1 on 2020-09-04 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200902_0013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['family'], 'verbose_name': 'Person'},
        ),
    ]
