# Generated by Django 4.1.5 on 2023-11-13 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_candidatequeue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidatequeue',
            name='number_of_vote',
        ),
    ]
