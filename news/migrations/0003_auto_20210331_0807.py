# Generated by Django 3.1 on 2021-03-31 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20210112_1856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='pic',
            new_name='picname',
        ),
        migrations.AddField(
            model_name='news',
            name='picurl',
            field=models.TextField(default='-'),
        ),
    ]
