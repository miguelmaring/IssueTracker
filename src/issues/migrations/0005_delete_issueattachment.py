# Generated by Django 4.1.7 on 2023-04-09 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0004_log_user_logs'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IssueAttachment',
        ),
    ]
