# Generated by Django 5.1 on 2024-10-15 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='support',
            old_name='typerequest',
            new_name='typerequest_id',
        ),
    ]
