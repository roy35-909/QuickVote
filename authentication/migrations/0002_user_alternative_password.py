# Generated by Django 4.2.6 on 2023-10-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='alternative_password',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]