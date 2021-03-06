# Generated by Django 3.1 on 2020-09-28 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0010_auto_20200917_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calculation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimated_consumption', models.FloatField(blank=True, null=True, verbose_name='Estimated Consumption [kWh]')),
                ('inverter_manufacturer', models.CharField(blank=True, max_length=500, null=True, verbose_name='Inverter Manufacturer')),
                ('module_manufacturer', models.CharField(blank=True, max_length=500, null=True, verbose_name='Module Manufacturer')),
                ('module_size', models.IntegerField(blank=True, null=True, verbose_name='Module Size')),
                ('estimated_dc_size', models.FloatField(blank=True, null=True, verbose_name='Estimated DC Size [kW]')),
                ('estimated_ac_size', models.FloatField(blank=True, null=True, verbose_name='Estimated AC Size [kW]')),
                ('estimated_modules', models.IntegerField(blank=True, null=True, verbose_name='Estimated Modules')),
                ('inverter_total_cost', models.FloatField(blank=True, null=True, verbose_name='Inverter Total Cost [USD]')),
                ('optimizer_unitary_cost', models.FloatField(blank=True, null=True, verbose_name='Optimizer Unitary Cost [USD]')),
                ('optimizer_total_cost', models.FloatField(blank=True, null=True, verbose_name='Optimizer Total Cost [USD]')),
                ('target_size', models.FloatField(blank=True, null=True, verbose_name='Target Size [kW]')),
                ('target_modules', models.IntegerField(blank=True, null=True, verbose_name='Target Modules')),
                ('module_cost_per_watt', models.FloatField(blank=True, null=True, verbose_name='Module Cost [$/W]')),
                ('module_total_cost', models.FloatField(blank=True, null=True, verbose_name='Module Total Cost [USD]')),
                ('module_degradation_per_year', models.CharField(blank=True, max_length=50, null=True, verbose_name='Module Degradation [%/yr]')),
                ('total_cost_per_watt', models.FloatField(blank=True, null=True, verbose_name='Total Cost [$/W]')),
                ('equipment_cost_per_watt', models.FloatField(blank=True, null=True, verbose_name='Equipment Cost [$/W]')),
                ('labor_cost_per_watt', models.FloatField(blank=True, null=True, verbose_name='Labor Cost [$/W]')),
                ('total_cost', models.FloatField(blank=True, null=True, verbose_name='Total Cost [USD]')),
                ('tmy3_specific_production', models.FloatField(blank=True, null=True, verbose_name='TMY3 Specific Production [kWh/kW/yr]')),
                ('prospector_specific_production', models.FloatField(blank=True, null=True, verbose_name='Prospector Specific Production [kWh/kW/yr]')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.project', verbose_name='Project')),
            ],
        ),
    ]
