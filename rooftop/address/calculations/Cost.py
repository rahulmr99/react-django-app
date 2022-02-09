import pandas as pd
import numpy as np
import os

from address.models import LaborBaseCost, LaborSize, LaborState

'''
This module's purpose is to calculate the total cost and cost per Watt of the estimated solar energy system

In order to do this, we import 3 CSV files:
1) Base Cost Sheet: Contains the base costs
2) Labor Size Sheet: Contains the additional labor costs incurred or reduced due to system size
3) Labor State Sheet: Contains the additional labor costs incurred or reduced due to state

Once we have all these CSV files, we proceed with the script.

Inputs:
strining_df -- the output of the size estimating module
state -- coming from the address input by the user

required inputs from each row of stringing_df (remember that each row is its own solar system configuration):
module cost $/W -- the cost per watt for just the modules of this system
total inverter cost -- the total inverter cost of this system
total optimizer cost -- the total optimizer cost of this system
--- together, the above three cost categories make up the equipment cost

dc size -- the total DC size of this system

Outputs:
cost_df -- a dataframe containing the following columns:
Labor Cost [$/W] -- the cost per watt for the labor of the construction of this system
Equipment Cost [$/W] -- the cost per watt for the equipment needed for this system
Total Cost [$/W] -- the total cost per watt of the system
Total Cost [USD] -- the total cost of the system

Once again, there is a row of the above dataframe for each system configuration

At the end of the script, we merge these two dataframes together to create a size_and_cost_df
'''

#import labor base cost 
# base_cost_sheet = pd.read_csv(os.path.join("address/calculations",'Labor Base Cost.csv'))

#import labor size sheet
# labor_size_sheet = pd.read_csv(os.path.join("address/calculations",'Labor Size.csv'))

#import labor state sheet
# labor_state_sheet = pd.read_csv(os.path.join("address/calculations",'Labor State.csv'))

#pull out the base labor cost from the base cost sheet
# base_labor_cost = float(list(base_cost_sheet[base_cost_sheet["Category"] == "Labor"]["Cost [$/W]"])[0].strip().strip('$'))

#pull out and sum all other costs from the base cost sheet (subtract labor)
# base_cost_per_watt = sum([float(item.strip().strip("$")) for item in list(base_cost_sheet["Cost [$/W]"])]) - base_labor_cost


def estimate_cost(stringing_df, state):
    '''
    This function takes stringing_df and state as inputs, and outputs a cost_df which computes the system costs for each system configuration
    In the next module, these costs will be used to calculate the financials of the system
    '''
    labor_base_costs = LaborBaseCost.objects.all()
    labor_sizes = LaborSize.objects.all()
    labor_states = LaborState.objects.all()
    
    base_labor_cost = float(labor_base_costs.get(category="Labor").cost.strip().strip('$'))
    base_cost_per_watt = sum([float(item.strip().strip("$")) for item in labor_base_costs.values_list('cost',flat=True)]) - base_labor_cost

    #pull the state labor adder from the state labor sheet
    # state_labor_adder = float(list(labor_state_sheet[labor_state_sheet["ST"] == state]["Labor Adder [$/W]"])[0].strip().strip("$"))
    state_labor_adder = float(labor_states.get(state=state).labor_adder_per_watt.strip().strip("$"))
    print("State Labor Adder [$/W]:", state_labor_adder)

    labor_costs, equipment_costs, total_costs_per_watt, total_costs = [],[],[],[]
    for row in stringing_df.index:
        #pull out variables for this row (each row is a system configuration from the size calculation module)
        module_cost_per_watt = stringing_df.at[row, "Module Cost [$/W]"]
        inverter_cost = stringing_df.at[row, "Inverter Total Cost [USD]"]
        optimizer_cost = stringing_df.at[row, "Optimizer Total Cost [USD]"]
        dc_size = stringing_df.at[row, "Estimated DC Size [kW]"]

        #calculate the per watt costs
        inverter_cost_per_watt = inverter_cost / (dc_size * 1000)
        optimizer_cost_per_watt = optimizer_cost / (dc_size * 1000)

        #add together all equipment cost per watt
        equipment_cost_per_watt = module_cost_per_watt + inverter_cost_per_watt + optimizer_cost_per_watt
        print("Equipment Cost Per Watt:", equipment_cost_per_watt)

        #find labor size adder
        try:
            # size_labor_adder = float(list(labor_size_sheet.loc[(labor_size_sheet["Min Size [kW]"] < dc_size) & (labor_size_sheet["Max Size [kW]"] > dc_size), "Adder"])[0])
            size_labor_adder = labor_sizes.get(min_size__lt=dc_size,max_size__gt=dc_size).adder
        except:
            size_labor_adder = 0.0
        print("Size Labor Adder for DC Size {}:".format(dc_size), size_labor_adder)

        #calculate labor cost
        labor_cost = base_labor_cost + state_labor_adder + size_labor_adder

        #find the total cost for this configuration
        total_cost_per_watt = base_cost_per_watt + equipment_cost_per_watt + labor_cost
        print("Total Cost Per Watt:", total_cost_per_watt)

        #calculate total cost
        total_cost = total_cost_per_watt * dc_size * 1000
        print("Total Cost:", total_cost)

        #save all items to lists
        total_costs_per_watt.append(total_cost_per_watt)
        equipment_costs.append(equipment_cost_per_watt)
        labor_costs.append(labor_cost)
        total_costs.append(total_cost)

    cost_df = pd.DataFrame({"Total Cost [$/W]": total_costs_per_watt, "Equipment Cost [$/W]": equipment_costs,
                            "Labor Cost [$/W]": labor_costs, "Total Cost [USD]": total_costs})

    return cost_df


# #import the output from the previous module
# stringing_df = pd.read_csv("Stringing DF.csv", index_col = 0)

# #run the module with an example state
# cost_df = estimate_cost(stringing_df, "NY")

# print(cost_df)

# #combine the inputs with the outputs to pass to the next module
# cost_and_size_df = pd.concat([stringing_df, cost_df], axis=1)

# print(cost_and_size_df)

# #save this as a CSV to pass to the next module
# cost_and_size_df.to_csv("Cost and Size DF.csv")
