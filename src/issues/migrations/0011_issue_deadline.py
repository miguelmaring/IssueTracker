# Generated by Django 4.1.7 on 2023-04-11 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0010_remove_issue_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]