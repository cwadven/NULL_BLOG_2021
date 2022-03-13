# Generated by Django 3.1.7 on 2022-03-13 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': '가입유형',
                'verbose_name_plural': '가입유형',
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '사용자', 'verbose_name_plural': '사용자'},
        ),
    ]
