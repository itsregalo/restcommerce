# Generated by Django 3.2.6 on 2021-08-20 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_productmedia_productimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='brief_describtion',
            new_name='brief_description',
        ),
        migrations.RenameField(
            model_name='productimage',
            old_name='media_content',
            new_name='image',
        ),
    ]
