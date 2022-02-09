# Generated by Django 3.1 on 2020-09-15 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '0007_auto_20200914_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to=settings.AUTH_USER_MODEL, verbose_name='Requested by'),
        ),
    ]