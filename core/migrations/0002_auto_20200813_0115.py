# Generated by Django 3.1 on 2020-08-12 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adress',
            options={'verbose_name': 'Adress'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Event'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Person'},
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name': 'Place'},
        ),
        migrations.AlterField(
            model_name='adress',
            name='coordinates',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='people',
            field=models.ManyToManyField(blank=True, null=True, to='core.Person'),
        ),
    ]