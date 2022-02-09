import csv
import json
from io import StringIO, BytesIO

from django.contrib.auth.models import User
from django.core.files.images import ImageFile #Handle bytes data of image

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status, viewsets
from rest_framework.response import Response


from users.models import User as RooftopUser

from address.serializers import RoofInfoSerializer, ProjectSerializer, CalculationSerializer
from address.models import  Project, Roof_info, Geocode, Calculation
from address.geocode import retrieveGeocodeData
from address.calculations.Calculate import Size, ProductionCost, Cost
class ProjectViewset(viewsets.ModelViewSet):
    """
    Create and List Project Details
    """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # list_serializer = CalculationSerializer

    def create(self, request, *args, **kwargs):
        projects = []
        for pjct in request.data:
            address = pjct.get('address')
            # image_bytes, url, formatted_address, lat, lon, state, zip_code = retrieveGeocodeData(address)

            # formatted_address, state = '682030, Infopark Campus, Kochi, Kerala 682030, India', 'KL'
            formatted_address, state = '9 Hardenburg Ln, East Brunswick, NJ 08816, USA', 'NJ'
            if not formatted_address == "Could not find specified address :/":
                stringing_inputs = {}
                roof_area = 5000000 # need to be calculated
                stringing_inputs.update({"roof_area":roof_area})
                openness = 0.90 # need to be calculated
                stringing_inputs.update({"openness":openness})
                task_target = "Consumption Offset" if pjct.get("task_target") == "CO" else ("Max Size" if pjct.get("task_target") == "MS" else None)  
                stringing_inputs.update({"task_target":task_target})

                stories = int(pjct.get("floors")) if pjct.get("floors") else None
                stringing_inputs.update({"stories":stories})

                consumption_per_area = 0.5 # need to be calculated
                stringing_inputs.update({"consumption_per_area":consumption_per_area})
                
                consumption_overwrite = float(pjct.get('consumption_overwrite')) if pjct.get('consumption_overwrite') else None
                stringing_inputs.update({"consumption_overwrite":consumption_overwrite})

                specific_production = 1350 # need to be calculated
                stringing_inputs.update({"specific_production":specific_production})
                stringing_df = Size(**stringing_inputs)
                cost_and_size_df = Cost(stringing_df)
                system_df = ProductionCost(cost_and_size_df,formatted_address=formatted_address,state=state)

                serializer = self.serializer_class(data=pjct)
                serializer.is_valid(raise_exception=True)
                if serializer.errors:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                p = serializer.save()
                # image = ImageFile(BytesIO(image_bytes), name='{}.jpg'.format(formatted_address)) # convert bytes to image
                # p.address_image = image
                # p.save()

                # Geocode.objects.create(
                #     project=p,
                #     lat=lat,
                #     lon=lon,
                #     state=state,
                #     zipcode=zip_code
                # )

                for row in system_df.index:
                    calculation = Calculation.objects.create(**{
                                    'project':p,
                                    'row': row,
                                    'estimated_consumption':system_df.at[row, "Estimated Consumption [kWh]"],
                                    'inverter_manufacturer':system_df.at[row, "Inverter Manufacturer"],
                                    'module_manufacturer':system_df.at[row, "Module Manufacturer"],
                                    'module_size':system_df.at[row, "Module Size"],
                                    'estimated_dc_size':system_df.at[row, "Estimated DC Size [kW]"],
                                    'estimated_ac_size':system_df.at[row, "Estimated AC Size [kW]"],
                                    'estimated_modules':system_df.at[row, "Estimated Modules"],
                                    'inverter_total_cost':system_df.at[row, "Inverter Total Cost [USD]"],
                                    'optimizer_unitary_cost':system_df.at[row, "Optimizer Unitary Cost [USD]"],
                                    'optimizer_total_cost':system_df.at[row, "Optimizer Total Cost [USD]"],
                                    'target_size': system_df.at[row, "Target Size [kW]"],
                                    'target_modules':system_df.at[row, "Target Modules"],
                                    'module_cost_per_watt':system_df.at[row, "Module Cost [$/W]"],
                                    'module_total_cost':system_df.at[row, "Module Total Cost [USD]"],
                                    'module_degradation_per_year':system_df.at[row, "Module Degradation [%/yr]"],
                                    'total_cost_per_watt':system_df.at[row, "Total Cost [$/W]"],
                                    'equipment_cost_per_watt':system_df.at[row, "Equipment Cost [$/W]"],
                                    'labor_cost_per_watt':system_df.at[row, "Labor Cost [$/W]"],
                                    'total_cost':system_df.at[row, "Total Cost [USD]"],
                                    'tmy3_specific_production':system_df.at[row, "TMY3 Specific Production [kWh/kW/yr]"],
                                    'prospector_specific_production':system_df.at[row, "Prospector Specific Production [kWh/kW/yr]"]
                    })
                projects.append(p)
        serialized_projects = self.get_serializer(projects, many=True)
        # headers = self.get_success_headers(serializer.data)
        return Response(serialized_projects.data, status=status.HTTP_201_CREATED,) #headers=headers)

    def list(self, *args, **kwargs):
        # user = self.request.query_params.get('user')
        # user_type = User.objects.get(id=user).type
        # print(user_type)
        # if user and user_type==2:
        #     self.queryset = Address.objects.filter(user__id=user)
        # self.serializer_class = self.list_serializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)


class RoofInfoViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RoofInfoSerializer
    queryset = Roof_info.objects.all()

# class InputFileUploadViewset(viewsets):

class UploadCSV(viewsets.ModelViewSet):
    """
    A view to parse csv and update data into google sheets
    """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                return Response({"status": "please input a csv file"}, status=status.HTTP_400_BAD_REQUEST)
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            csv_list = []
            for line in lines:
                s = StringIO(line)
                csv_line = list(csv.reader(s, skipinitialspace=True))
                csv_list.append(csv_line)
            record_list_final = []
            if csv_list[0][0][0].lower() == "client":
                del csv_list[0]
                for i in range(0, len(csv_list)-1):
                    if csv_list[i][0][0]=='' or csv_list[i][0][2]=='' or csv_list[i][0][3]=='':
                        data_status = False
                        return Response({"status": "required fields missing"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        data_status = True
                if data_status:
                    for i in range(0, len(csv_list)-1):
                        address = csv_list[i][0][3]
                        # image_bytes, url, formatted_address, lat, lon, state, zip_code = retrieveGeocodeData(address)
                        image = None
                        # image = ImageFile(BytesIO(image_bytes), name='{}.jpg'.format(formatted_address)) # convert bytes to image
                    projects = []
                    for i in range(0, len(csv_list)-1):
                        address = csv_list[i][0][3]
                        formatted_address, state = '9 Hardenburg Ln, East Brunswick, NJ 08816, USA', 'NJ'
                        if not formatted_address == "Could not find specified address :/":

                            stringing_inputs = {}
                            roof_area = 5000000 # need to be calculated
                            stringing_inputs.update({"roof_area":roof_area})
                            openness = 0.90 # need to be calculated
                            stringing_inputs.update({"openness":openness})

                            task_target = csv_list[i][0][6] if type(csv_list[i][0][6]) == str else ""
                            stringing_inputs.update({"task_target":task_target})
                            stories = csv_list[i][0][5] if type(csv_list[i][0][5]) == int else ""
                            stringing_inputs.update({"stories":stories})
                            consumption_per_area = 0.5 # need to be calculated
                            stringing_inputs.update({"consumption_per_area":consumption_per_area})
                            consumption_overwrite = csv_list[i][0][8] if type(csv_list[i][0][8]) == float else ""
                            stringing_inputs.update({"consumption_overwrite":consumption_overwrite})
                            specific_production = 1350 # need to be calculated
                            stringing_inputs.update({"specific_production":specific_production})
                            stringing_df = Size(**stringing_inputs)
                            cost_and_size_df = Cost(stringing_df)
                            system_df = ProductionCost(cost_and_size_df,formatted_address=formatted_address,state=state)

                            if csv_list[i][0][4] == "Office-Mixed Use":
                                csv_list[i][0][4] = "OMU"
                            else:
                                csv_list[i][0][4] = ""
                            if csv_list[i][0][5] == "":
                                csv_list[i][0][5] = None
                            if csv_list[i][0][6] == "Consumption Offset":
                                csv_list[i][0][6] = "CO"
                            elif csv_list[i][0][6] == "Max Size":
                                csv_list[i][0][6] = "MS"
                            else:
                                csv_list[i][0][6] == ""
                            if csv_list[i][0][8] == "":
                                csv_list[i][0][8] = None
                            if csv_list[i][0][9] == "":
                                csv_list[i][0][9] = None

                            csv_headers = ["client", "project_id", "project_name", "address", "building_type", "floors",
                            "task_target", "requested_by", "consumption_overwrite", "utility_overwrite"]
                            csv_record_dict = dict(zip(csv_headers, csv_list[i][0]))
                            serializer = self.serializer_class(data=csv_record_dict)
                            serializer.is_valid(raise_exception=True)
                            if serializer.errors:
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            project_ser = serializer.save()
                            projects.append(project_ser)
                    serialized_projects = self.get_serializer(projects, many=True)

                    for i in range(0, len(projects)):
                        for row in system_df.index:
                            calculation = Calculation.objects.create(**{
                                            'project': projects[i],
                                            'row': row,
                                            'estimated_consumption':system_df.at[row, "Estimated Consumption [kWh]"],
                                            'inverter_manufacturer':system_df.at[row, "Inverter Manufacturer"],
                                            'module_manufacturer':system_df.at[row, "Module Manufacturer"],
                                            'module_size':system_df.at[row, "Module Size"],
                                            'estimated_dc_size':system_df.at[row, "Estimated DC Size [kW]"],
                                            'estimated_ac_size':system_df.at[row, "Estimated AC Size [kW]"],
                                            'estimated_modules':system_df.at[row, "Estimated Modules"],
                                            'inverter_total_cost':system_df.at[row, "Inverter Total Cost [USD]"],
                                            'optimizer_unitary_cost':system_df.at[row, "Optimizer Unitary Cost [USD]"],
                                            'optimizer_total_cost':system_df.at[row, "Optimizer Total Cost [USD]"],
                                            'target_size': system_df.at[row, "Target Size [kW]"],
                                            'target_modules':system_df.at[row, "Target Modules"],
                                            'module_cost_per_watt':system_df.at[row, "Module Cost [$/W]"],
                                            'module_total_cost':system_df.at[row, "Module Total Cost [USD]"],
                                            'module_degradation_per_year':system_df.at[row, "Module Degradation [%/yr]"],
                                            'total_cost_per_watt':system_df.at[row, "Total Cost [$/W]"],
                                            'equipment_cost_per_watt':system_df.at[row, "Equipment Cost [$/W]"],
                                            'labor_cost_per_watt':system_df.at[row, "Labor Cost [$/W]"],
                                            'total_cost':system_df.at[row, "Total Cost [USD]"],
                                            'tmy3_specific_production':system_df.at[row, "TMY3 Specific Production [kWh/kW/yr]"],
                                            'prospector_specific_production':system_df.at[row, "Prospector Specific Production [kWh/kW/yr]"]
                            })

                    # Geocode.objects.create(
                    #     project=record,
                    #     lat=lat,
                    #     lon=lon,
                    #     state=state,
                    #     zipcode=zip_code
                    # )

                    return Response(serialized_projects.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "invalid csv format"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"status": "error in csv data"}, status=status.HTTP_400_BAD_REQUEST)