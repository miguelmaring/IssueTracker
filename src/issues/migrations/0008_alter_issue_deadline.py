# Generated by Django 4.1.7 on 2023-04-11 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0007_issue_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
