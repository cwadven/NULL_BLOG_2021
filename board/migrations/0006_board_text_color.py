# Generated by Django 3.1.7 on 2022-03-13 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_auto_20220313_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='text_color',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
