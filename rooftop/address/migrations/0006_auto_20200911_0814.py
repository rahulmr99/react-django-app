# Generated by Django 3.1 on 2020-09-11 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0005_auto_20200911_0626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='floors',
            field=models.IntegerField(verbose_name='Number of Floors'),
        ),
    ]
