# Generated by Django 4.2.1 on 2024-08-11 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_person_viaf_id_person_viaf_id_alternative_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='transliterated_name',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Транслитерированное имя'),
        ),
    ]