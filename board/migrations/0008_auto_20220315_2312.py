# Generated by Django 3.1.7 on 2022-03-15 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_board_info_background_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='text_color',
            new_name='info_text_color',
        ),
    ]
