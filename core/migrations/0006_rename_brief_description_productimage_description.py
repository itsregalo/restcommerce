# Generated by Django 3.2.6 on 2021-08-20 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210820_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='brief_description',
            new_name='description',
        ),
    ]