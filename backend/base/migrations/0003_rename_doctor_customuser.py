# Generated by Django 5.0.7 on 2024-07-19 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0002_rename_customuser_doctor'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Doctor',
            new_name='CustomUser',
        ),
    ]