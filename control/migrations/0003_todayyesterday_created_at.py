# Generated by Django 3.1.7 on 2022-03-05 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_ipvisitant_todayyesterday'),
    ]

    operations = [
        migrations.AddField(
            model_name='todayyesterday',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=False,
        ),
    ]
