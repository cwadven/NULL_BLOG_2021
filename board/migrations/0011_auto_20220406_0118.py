# Generated by Django 3.1.7 on 2022-04-06 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_auto_20220318_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]