# Generated by Django 2.2.4 on 2019-08-30 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': [('can_change', 'Can view, edit, delete or add books')]},
        ),
    ]
