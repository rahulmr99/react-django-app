# Generated by Django 3.1 on 2020-09-04 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('1', 'Admin'), ('2', 'Employee')], default='1', max_length=20),
        ),
    ]