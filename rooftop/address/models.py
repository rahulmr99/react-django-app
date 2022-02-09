from django.db import models
from users.models import User
# from django.contrib.auth.models import User

from django.utils.translation import gettext as _

class Coordinates(models.Model):
    """
    table for saving user address details
    """
    project = models.ForeignKey("address.Project", verbose_name=_("Project"), related_name="get_coordinates", on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'Address'


class Roof_info(models.Model):
    """
    Model for saving the roof info from ML calculations.
    """
    project = models.ForeignKey("address.Project", on_delete=models.CASCADE)
    total_area = models.FloatField()
    effective_area = models.FloatField()
    image = models.CharField(max_length=255, null=True, blank=True) #s3 link
    cost_calculation = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Roof Information'

class Project(models.Model):
    """
     Save all the data inputed during project creation
    """
    
    OFFICE_MIXED_USE = 'OMU'
    BUILDING_TYPE_CHOICES = [
        (OFFICE_MIXED_USE, 'Office-Mixed Use'),
    ]

    CONSUMPTION_OFFSET = 'CO'
    MAX_SIZE = 'MS'
    TASK_TARGET_CHOICES = [
        (CONSUMPTION_OFFSET,"Consumption Offset"),
        (MAX_SIZE, "Max Size")
    ]

    client = models.CharField(_("Client"), max_length=500)
    project_name = models.CharField(_("Project Name"), max_length=50)
    # address = models.ForeignKey("address.Address", verbose_name=_("Address"), on_delete=models.CASCADE)
    address = models.TextField(_("Address"),)
    building_type = models.CharField(_("Building Type"), choices=BUILDING_TYPE_CHOICES, max_length=150,\
        null=True,blank=True)
    floors = models.IntegerField(_("Number of Floors"),\
        null=True,blank=True)
    task_target = models.CharField(_("Task Target"), choices=TASK_TARGET_CHOICES, max_length=50,\
        null=True,blank=True)
    requested_by = models.ForeignKey(User, verbose_name=_("Requested by"), related_name='project', on_delete=models.CASCADE,\
        null=True,blank=True)
    consumption_overwrite = models.FloatField(_("Consumption Overwrite"),\
        null=True,blank=True)
    utility_overwrite = models.FloatField(_("Utility Overwrite"),\
        null=True,blank=True)
    address_image = models.ImageField(_("Address Image"), upload_to='AddressImages/',max_length=100,\
        null=True,blank=True)

    def __str__(self):
        return self.client
    

class Geocode(models.Model):
    project = models.ForeignKey("address.Project", verbose_name=_("Project"), related_name='get_map_data', on_delete=models.CASCADE)
    lat = models.CharField(_("Latitude"), max_length=50)
    lon = models.CharField(_("logitude"), max_length=50)
    state = models.CharField(_("State"), max_length=200)
    zipcode = models.CharField(_("Zipcode"), max_length=50)

class Calculation(models.Model):
    project = models.ForeignKey("address.Project", verbose_name=_("Project"), on_delete=models.CASCADE)
    row = models.IntegerField(_("Row in Dataframe"))
    estimated_consumption = models.FloatField(_("Estimated Consumption [kWh]"), null=True, blank=True)
    inverter_manufacturer = models.CharField(_("Inverter Manufacturer"), max_length=500, null=True, blank=True)
    module_manufacturer = models.CharField(_("Module Manufacturer"), max_length=500, null=True, blank=True)
    module_size = models.IntegerField(_("Module Size"), null=True, blank=True)
    estimated_dc_size = models.FloatField(_("Estimated DC Size [kW]"), null=True, blank=True)
    estimated_ac_size = models.FloatField(_("Estimated AC Size [kW]"), null=True, blank=True)
    estimated_modules = models.IntegerField(_("Estimated Modules"), null=True, blank=True)
    inverter_total_cost = models.FloatField(_("Inverter Total Cost [USD]"), null=True, blank=True)
    optimizer_unitary_cost = models.FloatField(_("Optimizer Unitary Cost [USD]"), null=True, blank=True)
    optimizer_total_cost = models.FloatField(_("Optimizer Total Cost [USD]"), null=True, blank=True)
    target_size = models.FloatField(_("Target Size [kW]"), null=True, blank=True)
    target_modules = models.IntegerField(_("Target Modules"), null=True, blank=True)
    module_cost_per_watt = models.FloatField(_("Module Cost [$/W]"), null=True, blank=True)
    module_total_cost = models.FloatField(_("Module Total Cost [USD]"), null=True, blank=True)
    module_degradation_per_year = models.CharField(_("Module Degradation [%/yr]"), max_length=50, null=True, blank=True)
    total_cost_per_watt = models.FloatField(_("Total Cost [$/W]"), null=True, blank=True)
    equipment_cost_per_watt = models.FloatField(_("Equipment Cost [$/W]"), null=True, blank=True)
    labor_cost_per_watt = models.FloatField(_("Labor Cost [$/W]"), null=True, blank=True)
    total_cost = models.FloatField(_("Total Cost [USD]"), null=True, blank=True)
    tmy3_specific_production = models.FloatField(_("TMY3 Specific Production [kWh/kW/yr]"), null=True, blank=True)
    prospector_specific_production = models.FloatField(_("Prospector Specific Production [kWh/kW/yr]"), null=True, blank=True)

    def __str__(self):
        return self.project.project_name + "-" + str(self.row)

class InverterStringing(models.Model):
    inverter_manufacturer = models.CharField(_("Inverter Manufacturer"), max_length=150, null=True, blank=True)
    model = models.CharField(_("Model"), max_length=150, null=True, blank=True)
    ac_size = models.FloatField(_("AC Size [kW]"), null=True, blank=True)
    priority_rank = models.IntegerField(_("Priority Rank"), null=True, blank=True)
    number_of_strings = models.IntegerField(_("Number of Strings"), null=True, blank=True)
    module_manufacturer = models.CharField(_("Module Manufacter"), max_length=150, null=True, blank=True)
    module_size = models.IntegerField(_("Module Size [W]"), null=True, blank=True)
    module_per_string = models.IntegerField(_("Modules per String"), null=True, blank=True)
    total_modules = models.IntegerField(_("Total Modules"), null=True, blank=True)
    inverter_unit_cost = models.FloatField(_("Inverter Unit Cost [USD]"), null=True, blank=True)
    module_cost_per_watt = models.FloatField(_("Module Cost [USD/W]"), null=True, blank=True)
    optimizer_unit_price = models.FloatField(_("Optimizer Unit Price [USD]"), null=True, blank=True)
    module_area_at_5_degree_tilt = models.FloatField(_("Module Area at 5° Tilt [sqf]"), null=True, blank=True)
    module_degradation = models.CharField(_("Module Degradation [%/Year]"), max_length=50, null=True, blank=True)

    def __str__(self):
        return "{}-{}-{}".format(self.inverter_manufacturer, self.model, self.module_manufacturer)

# Code,Category,Cost [$/W]
class LaborBaseCost(models.Model):
    code = models.IntegerField(_("Code"))
    category = models.CharField(_("Category"), max_length=150)
    cost = models.CharField(_("Cost"), max_length=50)

class LaborSize(models.Model):
    min_size = models.IntegerField(_("Min Size [kW]"))
    max_size = models.IntegerField(_("Max Size [kW]"))
    adder = models.FloatField(_("Adder"))

class LaborState(models.Model):
    state = models.CharField(_("ST"), max_length=50)
    labor_adder_per_watt = models.CharField(_("Labor Adder [$/W]"), max_length=50)
    region = models.CharField(_("Region"), max_length=250)

class ProductionLossesByST(models.Model):
    state = models.CharField(_("ST"), max_length=50)
    snow = models.CharField(_("Snow"), max_length=50)
    soiling = models.CharField(_("Soiling"), max_length=50)
    downtime = models.CharField(_("Downtime"), max_length=50)
    ac_losses = models.CharField(_("AC Losses"), max_length=50)
    shading = models.CharField(_("Shading"), max_length=50)
    total_losses = models.CharField(_("Total Losses [%]"), max_length=50)