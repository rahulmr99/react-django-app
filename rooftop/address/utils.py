from calculations.Size import calculate_stringing
from calculations.Cost import estimate_cost
from calculations.Production import calculate_prospector_and_tmy3
from geocode import GoogleGeocode, getStatefromJSON, getFormattedAddressfromJSON

def Size(roof_area=5000000, openness=0.90, task_target = "Consumption Offset", consumption_per_area = 0.5,\
    stories = 1, consumption_overwrite = None, specific_production = 1350):
    stringing_df = calculate_stringing(roof_area, openness, task_target, consumption_per_area,
                        stories, consumption_overwrite, specific_production)

    print(stringing_df)
    print(stringing_df["Estimated DC Size [kW]"])

    # stringing_df.to_csv("Stringing DF.csv")
    return stringing_df

def Cost(stringing_df):
    #import the output from the previous module
    # stringing_df = pd.read_csv("Stringing DF.csv", index_col = 0)

    #run the module with an example state
    cost_df = estimate_cost(stringing_df, "NY")

    print(cost_df)

    #combine the inputs with the outputs to pass to the next module
    cost_and_size_df = pd.concat([stringing_df, cost_df], axis=1)

    print(cost_and_size_df)

    #save this as a CSV to pass to the next module
    # cost_and_size_df.to_csv("Cost and Size DF.csv")
    return cost_and_size_df

def ProductionCost(cost_and_size_df):
    address = "1407 Broadway, New York, NY"

    geocode_response = GoogleGeocode(parse_address(address))

    state = getStatefromJSON(geocode_response)
    formatted_address = getFormattedAddressfromJSON(geocode_response)

    prospector_specific, tmy3_specific, prospector_monthly, tmy3_monthly = calculate_prospector_and_tmy3(formatted_address, state)

    print("TMY3 Specific Production:", np.round(tmy3_specific, 2), "kWh/kW/yr")
    print("Prospector Specific Production:", np.round(prospector_specific, 2), "kWh/kW/yr")

    tmy_specific_productions = [tmy3_specific] * len(cost_and_size_df)
    prospector_specific_productions = [prospector_specific] * len(cost_and_size_df)

    #create a dataframe for the specific production
    specific_production_df = pd.DataFrame({"TMY3 Specific Production [kWh/kW/yr]": tmy_specific_productions,
                                        "Prospector Specific Production [kWh/kW/yr]": prospector_specific_productions})

    #add the two dataframes together
    # system_df = pd.concat([cost_and_size_df, specific_production_df], axis = 1)

    system_df.to_csv("System DF.csv")
    return {}

def CalculateValues():
    stringing_df = Size()
    cost_and_size_df = Cost(stringing_df)
    system_df = ProductionCost(cost_and_size_df)
    print(system_df)

if __name__ == "__main__":
    CalculateValues()