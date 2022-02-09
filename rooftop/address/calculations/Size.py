# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os

from address.models import InverterStringing

#import the CSV that holds the inverter stringing calculations
# inverter_sheet = pd.read_csv(os.path.join("address/calculations",'Inverter Stringing.csv'))

#define a function to get cell by column name
# def get_inverter_cell_by_column_name(row, column_name):
#     return inverter_sheet.at[row, column_name]

#define a function to compile lists of inverters, modules, and manufacturers from the CSV
def create_inverter_and_module_lists():
    #create lists of inverters, inverter manufacturers, and modules from our Inverter Stringing CSV
    all_inverters, all_inverter_manufacturers, all_modules = [],[],[]
    
    # for row in inverter_sheet.index:
    #     inv_manufacturer = get_inverter_cell_by_column_name(row, "Inverter Manufacturer")
    #     inv_size = get_inverter_cell_by_column_name(row, "AC Size [kW]")

    #     mod_manufacturer = get_inverter_cell_by_column_name(row, "Module Manufacter")        
    #     mod_size = get_inverter_cell_by_column_name(row, "Module Size [W]")
    #     mod_area = get_inverter_cell_by_column_name(row, "Module Area at 5° Tilt [sqf]")
    
    inverter_stringing_objs = InverterStringing.objects.all()
    for obj in inverter_stringing_objs:
        inv_manufacturer = obj.inverter_manufacturer
        inv_size = obj.ac_size

        mod_manufacturer = obj.module_manufacturer        
        mod_size = obj.module_size
        mod_area = obj.module_area_at_5_degree_tilt

    
        #we don't need SMA inverters for now
        # if(pd.isna(inv_size) == False and inv_manufacturer != "SMA"):
        #     inverter_specs = (inv_manufacturer, inv_size)
        #     module_specs = (mod_manufacturer, mod_size, mod_area)

        #     all_inverters.append(inverter_specs)
        #     all_modules.append(module_specs)
        #     all_inverter_manufacturers.append(inv_manufacturer)
        
        if inv_size and inv_manufacturer != "SMA":
            inverter_specs = (inv_manufacturer, inv_size)
            module_specs = (mod_manufacturer, mod_size, mod_area)

            all_inverters.append(inverter_specs)
            all_modules.append(module_specs)
            all_inverter_manufacturers.append(inv_manufacturer)

    
    inverters = list(set(all_inverters))
    modules = list(set(all_modules))
    inverter_manufacturers = list(set(all_inverter_manufacturers))
    
    return inverters, modules, inverter_manufacturers

#create a dictionary of inverter manufacturers to their inverters
def create_inverter_dict(inverter_manufacturers, inverters):
    inverter_dict = {}
    for inverter_manufacturer in inverter_manufacturers:
        inverters_by_manufacturer = []
        for inverter in inverters:
            if(inverter[0] == inverter_manufacturer):
                inverters_by_manufacturer.append(inverter)

        inverters_by_manufacturer = sorted(inverters_by_manufacturer, key=lambda x: x[1], reverse=True)
                
        inverter_dict[inverter_manufacturer] = inverters_by_manufacturer
    
    return inverter_dict

#define a function to pull a specific inverter-module combination from the Inverter Stringing CSV
def pull_inverter_module_specs(inverter_manufacturer, inverter_size, module_manufacturer, module_size):
    #this function pulls the specs for a given inverter-module combination from the Inverter Stringing CSV
    # for row in inverter_sheet.index:
    #     inv_manufacturer = get_inverter_cell_by_column_name(row, "Inverter Manufacturer")
    #     inv_size = get_inverter_cell_by_column_name(row, "AC Size [kW]")

    #     mod_manufacturer = get_inverter_cell_by_column_name(row, "Module Manufacter")
    #     mod_size = get_inverter_cell_by_column_name(row, "Module Size [W]")
    
    invert_stringing_objs = InverterStringing.objects.all()
    for obj in invert_stringing_objs:
        inv_manufacturer = obj.inverter_manufacturer
        inv_size = obj.ac_size

        mod_manufacturer =  obj.module_manufacturer
        mod_size = obj.module_size
                
        if(inv_manufacturer == inverter_manufacturer and inv_size == inverter_size):
            if(mod_size == module_size and mod_manufacturer == module_manufacturer):
                # inv_num_strings = get_inverter_cell_by_column_name(row, "Number of Strings")
                # inv_mod_per_string = get_inverter_cell_by_column_name(row, "Modules per String")
                # inv_unit_cost = get_inverter_cell_by_column_name(row, "Inverter Unit Cost [USD]")
                # optimizer_cost = get_inverter_cell_by_column_name(row, "Optimizer Unit Price [USD]")

                # mod_area = get_inverter_cell_by_column_name(row, "Module Area at 5° Tilt [sqf]")
                # mod_cost_per_watt = get_inverter_cell_by_column_name(row, "Module Cost [USD/W]")
                # mod_degradation = get_inverter_cell_by_column_name(row, "Module Degradation [%/Year]")

                inv_num_strings = obj.number_of_strings
                inv_mod_per_string = obj.number_of_strings
                inv_unit_cost =  obj.inverter_unit_cost
                optimizer_cost = obj.optimizer_unit_price

                mod_area = obj.module_area_at_5_degree_tilt
                mod_cost_per_watt = obj.module_cost_per_watt
                mod_degradation = obj.module_degradation
    
                inverter_module_specs = [inv_num_strings, inv_mod_per_string, inv_unit_cost, optimizer_cost,
                                         mod_area, mod_cost_per_watt, mod_degradation]
        
    return inverter_module_specs

def calculate_stringing(roof_area, openness, task_target, consumption_per_area,
                        stories, consumption_overwrite, specific_production):
    """This function computes the possible stringing options for the solar energy system.

    Inputs:
    task_target -- if "Max Fit", then we fill the roof with the maximum number of modules
                   if "Consumption Offset", then we create a system to produce 90% of the building's energy consumption
    
    roof_area -- the total roof area of all buildings in the address
    openness -- the percentage of the roof which is usable to put solar modules on

    The rest of the inputs are only used if task_target is "Consumption Offset"

    consumption_per_area -- the estimated amount of energy used per unit area of the building
    stories -- number of stories or floors in the building
    consumption_overwrite -- if the user knows the building consumption beforehand, they can input it
                             and it will overwrite our estimated consumption
    specific_production -- a measure of the amount of energy produced by each kW of solar panels installed on the roof
    
    Outputs:
    The function tries several different configurations of solar modules and inverters and comes up with a row for each
    configuration in the returned dataframe stringing_df

    stringing_df -- a dataframe containing the following columns:

        "Estimated Consumption [kWh]": our estimate of the building's annual energy consumption (same for all configurations--only used if task_target is "Consumption Offset") 
        "Inverter Manufacturer": the manufacturer of the inverters for this configuration
        "Module Manufacturer": the manufacturer of the modules for this configuration
        "Module Size": the size of the modules for this configuration
        "Estimated DC Size": the estimated DC size for this configuration (number of modules * module size = DC size)
        "Estimated AC Size": the estimated AC size for this configuration (number of inverters * inverter size = AC size)
        "Estimated Modules": the estimated number of modules for this configuration
        "Inverter Total Cost [USD]": the total cost of inverters for this configuration
        "Optimizer Unitary Cost [USD]": the unit cost of optimizers for this configuration (follows inverter manufacturer)
        "Optimizer Total Cost [USD]": the total cost of optimizers for this configuration
        "Target Size": the target DC size required to hit the consumption or to max out the rooftop
        "Target Modules": the target number of modules needed to match the target size
        "Module Cost [$/W]": cost per watt of the modules for this configuration
        "Module Total Cost [USD]": total cost of the modules for this configuration
        "Module Degradation [%/Year]": module degradation of the modules for this configuration
    """
    #PROJECT LEVEL CALCS
    
    #find useable roof area using openness and total roof area
    useable_area = (roof_area * (openness / 100))

    #check if stories is correctly input
    if(stories is None):
        stories = 1
    elif(type(stories) != int):
        stories = 1
    elif(stories == 0):
        stories = 1
    
    #check for consumption overwrite, if none then calculate consumption by area
    if (consumption_overwrite == '' or consumption_overwrite is None or consumption_overwrite <= 0):
        #we can match up to 90% of the building's annual energy consumption with estimated solar energy production
        estimated_consumption = roof_area * stories * consumption_per_area * 0.9
    else: 
        estimated_consumption = consumption_overwrite
    
    #calculate target size if consumption offset
    consumption_size = estimated_consumption / specific_production
    
    print("Consumption Size:", consumption_size)

    #INVERTER/MODULE FOR LOOP
    #calculate the all the outputs for each configuration of modules and inverters
    estimated_dc_sizes, estimated_modules_list, optimizer_total_costs = [],[],[]
    estimated_ac_sizes, inverter_total_costs = [],[]
    module_manufacturers_list, inverter_manufacturers_list, module_sizes = [],[],[]
    target_sizes, target_modules_list = [],[]
    module_costs, module_degradations, module_total_costs, optimizer_unit_costs = [],[],[],[]
    for inverter_manufacturer in inverter_manufacturers:
        
        #select all inverters from manufacturer and their sizes
        inverters = inverter_dict[inverter_manufacturer]
        inverters = sorted(inverters, key=lambda x: x[1], reverse=True)

        #loop over all modules
        for module in modules:
            module_manufacturer = module[0]
            module_size = module[1]
            module_area = module[2]
            
            #calculate max fit and consumption modules
            max_fit_modules = np.floor(useable_area / module_area)
            max_fit_size = max_fit_modules * (module_size / 1000)
            consumption_modules = np.floor(consumption_size / (module_size / 1000))
            
            print("Max Fit Size:", max_fit_size)

            #check for task target and select appropriate target size and modules
            if(task_target == "Max Size" or "MS" or task_target is None):
                target_size = max_fit_size
                target_modules = max_fit_modules
            elif(task_target == "Consumption Offset" or "CO"):
                if(max_fit_size < consumption_size):
                    target_size = max_fit_size
                    target_modules = max_fit_modules
                else:
                    target_size = consumption_size
                    target_modules = consumption_modules

            print("Target Size:", target_size)
            residual_modules = target_modules
            inverter_counts, inverter_unit_costs = {},{}
            #pull stringing details for each inverter/module combination
            for i in range(len(inverters)):
                inverter = inverters[i]
                inverter_manufacturer = inverter[0]
                inverter_size = inverter[1]
            
                #pull inverter module specs
                inverter_module_specs = pull_inverter_module_specs(inverter_manufacturer, inverter_size,
                                                                   module_manufacturer, module_size)
                
                #unpack specs
                inv_num_strings = inverter_module_specs[0]
                inv_mod_per_string = inverter_module_specs[1]
                inv_unit_cost = inverter_module_specs[2]
                optimizer_cost = inverter_module_specs[3]
                mod_area = inverter_module_specs[4]
                mod_cost_per_watt = inverter_module_specs[5]
                mod_degradation = inverter_module_specs[6]
                
                #save inverter unit costs
                inverter_unit_costs[inverter_size] = inv_unit_cost
                
                #calculate modules per inverter
                inverter_max_modules = inv_num_strings * inv_mod_per_string
                
                #check if another inverter can be added
                if(residual_modules > inverter_max_modules):
                    #if so, calculate the number of this inverter to add
                    num_inverters = np.floor(residual_modules / inverter_max_modules)
                    
                    #store the result in inverter counts
                    inverter_counts[inverter_size] = num_inverters
                
                    #decrement residual modules
                    residual_modules = residual_modules % inverter_max_modules
            
            #calculate the estimated modules, DC size, module total cost, and optimizer total cost
            estimated_modules = target_modules
            estimated_dc_size = estimated_modules * (module_size/1000)
            module_total_cost = estimated_dc_size * mod_cost_per_watt * 1000
            if(optimizer_cost is not None):
                optimizer_total_cost = np.ceil((estimated_modules / 2) * optimizer_cost)
            else:
                optimizer_total_cost = 0
            
            #calculate the estimated AC size and inverter cost
            estimated_ac_size, inverter_total_cost = 0,0
            for inverter_ac_size in list(inverter_counts.keys()):
                num_inverters = inverter_counts[inverter_ac_size]
                estimated_ac_size += (num_inverters * inverter_ac_size)
                inverter_unit_cost = inverter_unit_costs[inverter_ac_size]
                inverter_total_cost += inverter_unit_cost * num_inverters
            
            #store estimated modules, DC size, and optimizer total cost
            estimated_modules_list.append(int(estimated_modules))            
            estimated_dc_sizes.append(estimated_dc_size)
            optimizer_unit_costs.append(optimizer_cost)
            optimizer_total_costs.append(optimizer_total_cost)
            
            #store estimated AC size and unit cost
            estimated_ac_sizes.append(estimated_ac_size)
            inverter_total_costs.append(inverter_total_cost)
            
            #store inverter and module manufacturers and module size
            inverter_manufacturers_list.append(inverter_manufacturer)
            module_manufacturers_list.append(module_manufacturer)
            module_sizes.append(int(module_size))
            
            #store target size and target modules
            target_sizes.append(target_size)
            target_modules_list.append(int(target_modules))
            
            #store module cost and degradation
            module_costs.append(mod_cost_per_watt)
            module_degradations.append(mod_degradation)
            module_total_costs.append(module_total_cost)
            
    #store results in a dictionary
    stringing_dict = {
        "Estimated Consumption [kWh]": [estimated_consumption]*len(module_sizes), 
        "Inverter Manufacturer": inverter_manufacturers_list,
        "Module Manufacturer": module_manufacturers_list,
        "Module Size": module_sizes,
        "Estimated DC Size [kW]": estimated_dc_sizes,
        "Estimated AC Size [kW]": estimated_ac_sizes,
        "Estimated Modules": estimated_modules_list,
        "Inverter Total Cost [USD]": inverter_total_costs,
        "Optimizer Unitary Cost [USD]": optimizer_unit_costs,
        "Optimizer Total Cost [USD]": optimizer_total_costs,
        "Target Size [kW]": target_sizes,
        "Target Modules": target_modules_list,
        "Module Cost [$/W]": module_costs,
        "Module Total Cost [USD]": module_total_costs,
        "Module Degradation [%/yr]": module_degradations
    }

    #return a dataframe of the above dictionary
    stringing_df = pd.DataFrame(stringing_dict)
            
    return stringing_df

#create lists of modules and inverters
inverters, modules, inverter_manufacturers = create_inverter_and_module_lists()
inverter_dict = create_inverter_dict(inverter_manufacturers, inverters)

#EXAMPLE VALUES
# roof_area = 5000000
# openness = 0.90
# task_target = "Consumption Offset"
# consumption_per_area = 0.5
# stories = 1
# consumption_overwrite = None
# specific_production = 1350

# stringing_df = calculate_stringing(roof_area, openness, task_target, consumption_per_area,
#                     stories, consumption_overwrite, specific_production)

# print(stringing_df)
# print(stringing_df["Estimated DC Size [kW]"])

# stringing_df.to_csv("Stringing DF.csv")