# Generated by Django 3.1 on 2021-05-14 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('cm', models.TextField()),
                ('newsid', models.IntegerField()),
                ('date', models.CharField(max_length=50)),
                ('time', models.CharField(max_length=50)),
            ],
        ),
    ]
