# Generated by Django 4.1.7 on 2023-04-11 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0009_alter_issue_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='deadline',
        ),
    ]