from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Coordinates, Roof_info, Project, Geocode, Calculation,\
                    InverterStringing, LaborBaseCost, LaborSize, LaborState,\
                        ProductionLossesByST

admin.site.register(Coordinates)
admin.site.register(Roof_info)
admin.site.register(Project)
admin.site.register(Geocode)
admin.site.register(Calculation)

@admin.register(InverterStringing)
class InverterStringingAdmin(ImportExportModelAdmin):
    pass

@admin.register(LaborBaseCost)
class LaborBaseCostAdmin(ImportExportModelAdmin):
    pass

@admin.register(LaborSize)
class LaborSizeAdmin(ImportExportModelAdmin):
    pass

@admin.register(LaborState)
class LaborStateAdmin(ImportExportModelAdmin):
    pass

@admin.register(ProductionLossesByST)
class ProductionLossesBySTAdmin(ImportExportModelAdmin):
    pass