# Generated by Django 4.2.1 on 2024-08-11 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_person_transliterated_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='viaf_name',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='VIAF Name'),
        ),
    ]