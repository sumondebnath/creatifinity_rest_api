# Generated by Django 5.0.1 on 2024-04-05 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_rename_user_useraccount_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='account',
            new_name='user',
        ),
    ]
