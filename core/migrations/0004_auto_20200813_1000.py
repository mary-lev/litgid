# Generated by Django 3.1 on 2020-08-13 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200813_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='people',
            field=models.ManyToManyField(blank=True, to='core.Person'),
        ),
    ]
