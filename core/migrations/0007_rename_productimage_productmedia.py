# Generated by Django 3.2.6 on 2021-08-20 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_brief_description_productimage_description'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductImage',
            new_name='ProductMedia',
        ),
    ]
