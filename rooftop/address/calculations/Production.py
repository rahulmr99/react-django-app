import pandas as pd
import numpy as np
import requests
import json
import os

from address.models import ProductionLossesByST

#insert your Google Cloud Platform API Key here
API_KEY = "AIzaSyARoizs3vxF0OBbTqL10Ry7be2CUtALamE"

#insert your NREL Developer API Key here
NREL_KEY = "dtAPfTqKxyFQag2XPdaQz2j9uGnQR2kAgfeykTNT"

#import the output from the previous modules
# cost_and_size_df = pd.read_csv(os.path.join("address/calculations","Cost and Size DF.csv"))

def get_state_loss(state):
    return float(ProductionLossesByST.objects.get(state=state).total_losses.strip("%"))

#Global Variables
system_capacity = 88.8
gcr = 0.4
dc_ac_ratio = 1.35
inv_eff = 98
losses = 16.5
tilt = 5
azimuth = 180

#define a list of all Class I Sites
Class_I_Sites = ['722280','723230','722230','722260','723403','722780','723723','722740','725945','723840','723815','723890',
                 '722970','722950','725920','724830','722900','724940','723925','723940','725650','724760','724665','725040',
                 '725080','724089','722056','722106','722146','722060','722010','722020','722050','722223','722140','722110',
                 '722045','723110','722190','722180','722255','722170','722070','912850','911820','911900','911650','726810',
                 '727830','725780','725300','725440','725320','725430','724390','724320','725330','724380','725350','725460',
                 '725470','725485','725570','725480','724585','724210','724236','724220','724230','724350','722400','722310',
                 '722480','726088','727120','726060','724060','725090','725095','726390','725375','725370','726370','726350',
                 '726380','725390','726360','727340','726387','727450','727470','726580','726440','726550','722350','722340',
                 '724450','724460','724400','724340','724345','726770','727680','727750','727720','727790','727730','725560',
                 '725620','725500','725660','725670','724860','723860','725805','723870','724880','724855','725830','726050',
                 '724070','725020','723650','723627','722680','725180','725150','725280','725035','726223','744860','725030',
                 '725290','725190','723150','723040','723140','723170','723060','723013','727640','727530','727676','727670',
                 '725210','725240','724280','724290','725246','725360','725250','726930','725970','726880','726980','726940',
                 '725170','725266','725260','725115','724080','725200','725130','725140','725070','722080','723100','723120',
                 '726590','726540','726686','726620','726510','723183','723240','723260','723340','723270','722660','722540',
                 '722500','722510','722590','722700','722430','722670','722446','722650','722410','722630','722530','722550',
                 '722560','724755','725720','726170','724100','723080','724010','724110','724030','724050','727920','727970',
                 '727930','727850','727810','724120','724140','724170','724250','726435','726450','726430','726410','726400',
                 '725690','725640','725760','725744','726660']

def parse_address(address_field):
    #take in an address or a lat, lon coordinate pair and return an address and a tag
    #inputs: address or coordinates
    #outputs: address or coordinates with tag
    if("(" in address_field and ")" in address_field):
        left = address_field.find("(")
        right = address_field.find(")")
        coordinates = address_field[left+1:right]
        if("," in coordinates):
            if(coordinates.count(".") == 2):
                coordinates = coordinates.replace(" ","")
                return coordinates, "Coordinates"
            else:
                return address_field, "Address"
        else:
            return address_field, "Address"
    else:
        return address_field, "Address"

#define a function to get the JSON response for a Google Geocode API request
def GoogleGeocode(address_details):
    #geocode an address using Google Geocoding API
    #inputs: address and tag
    #outputs: api response dictionary
    url = "https://maps.googleapis.com/maps/api/geocode/json?key={}".format(API_KEY)
    
    address = address_details[0]
    address_type = address_details[1]
    
    if(address_type == "Address"):
        address = address.replace(" ", "+")
        url += ("&address=" + address)
        
    if(address_type == "Coordinates"):
        url += ("&latlng=" + address)
    
    response = requests.get(url)
    json_response = json.loads(response.text)
    return json_response

#define functions to get site coordinates from the JSON response
def getLatfromJSON(json_response):
    lat = json_response['results'][0]['geometry']['location']['lat']
    return lat

def getLonfromJSON(json_response):
    lon = json_response['results'][0]['geometry']['location']['lng']
    return lon

#define function to get state from the JSON response
def getStatefromJSON(json_response):
    state = ""
    
    for level in json_response['results'][0]['address_components']:
        level_type = level['types'][0]
        if(level_type == "administrative_area_level_1"):
            state = level['short_name']
    
    return state

def getFormattedAddressfromJSON(json_response):
    return json_response['results'][0]['formatted_address']

#define a function to issue a get request to NREL's Solar Dataset Query API
def solar_database_request(address):
    #set the base URL, including our API key and the preferred output format of JSON
    url = "https://developer.nrel.gov/api/solar/data_query/v1.json?api_key={}&format=JSON&all=1".format(NREL_KEY)
    #set the radius of our request to 100 miles (pull all weather stations within 100 mi)
    radius = 2000
    
    #add the radius and address to our URL
    url += ("&radius=" + str(radius))
    url += ("&address=" + str(address))
    
    #issue the get request via Python's requests library
    response = requests.get(url)
    json_response = json.loads(response.text)
    json_data = json_response['outputs']

    #return the JSON response
    return json_data

#define a function to issue a get request to NREL's PVWatts API including azimuth and tilt
def pvwatts_request(file_id, losses, azimuth, tilt, system_capacity, gcr):
    #set the base URL, including our API key and the preferred output format of JSON
    url = "https://developer.nrel.gov/api/pvwatts/v6.json?api_key={}".format(NREL_KEY)
    #set the static parameters
    module_type = 1
    array_type = 1
    azimuth = azimuth
    tilt = tilt
    ID = file_id
    losses = losses
    system_capacity = system_capacity
    radius = 0
    dc_ac_ratio = 1.32
    gcr = gcr
    inv_eff = 98
    
    #append the static parameters and the file ID to our URL
    url += ("&system_capacity=" + str(system_capacity))
    url += ("&file_id=" + str(ID))
    url += ("&module_type=" + str(module_type))
    url += ("&array_type=" + str(array_type))
    url += ("&azimuth=" +str(azimuth))
    url += ("&tilt=" +str(tilt))
    url += ("&losses=" +str(losses))
    url += ("&radius=" +str(radius))
    url += ("&dc_ac_ratio=" +str(dc_ac_ratio))
    url += ("&gcr=" +str(gcr))
    url += ("&inv_eff=" +str(inv_eff))
    
    #issue the get request via Python's requests library
    response = requests.get(url)
    json_response = json.loads(response.text)

    #return the specific production
    specific_production = json_response['outputs']['ac_annual']/system_capacity
    
    monthly_production = json_response['outputs']['ac_monthly']
    
    return specific_production, monthly_production

def parse_solar_dataset_response(response):
    #Find the appropriate file IDs from the API response
    tmy3_file_ids = []
    for station in response["all_stations"]:
        trimmed_id = station["id"][2:]
        if(station["dataset"] == "nsrdb"):
            prospector_file_id = station["id"]
        if(trimmed_id in Class_I_Sites):
            tmy3_file_ids.append(station["id"])
    try:    
        tmy3_file_id = tmy3_file_ids[0]
    except IndexError:
        raise Exception("Staion Id not found")
    
    return prospector_file_id, tmy3_file_id

def calculate_prospector_and_tmy3(address, state):
    #query the NSRDB database
    solar_dataset_query_response = solar_database_request(address)
    
    #parse the NSRDB database response to find the appropriate prospector and tmy3 class I data files
    prospector_file_id, tmy3_file_id = parse_solar_dataset_response(solar_dataset_query_response)
    
    #retrieve losses from state loss dictionary
    losses = get_state_loss(state)
    
    #calculate pvwatts requests for both prospector and tmy3
    prospector_specific, prospector_monthly = pvwatts_request(prospector_file_id, losses, azimuth, tilt, system_capacity, gcr)
    tmy3_specific, tmy3_monthly = pvwatts_request(tmy3_file_id, losses, azimuth, tilt, system_capacity, gcr)
        
    return prospector_specific, tmy3_specific, prospector_monthly, tmy3_monthly

'''
Inputs: 
losses_sheet -- a dataframe created from the CSV file containing the production losses of each state 
address -- from the user's input. We must take the state from this address using GoogleGeocode function
cost_and_size_df -- the output from the previous modules

Outputs:
TMY3 specific production -- a measure of the system's energy production per unit power per year, calculated using TMY3 ground based weather data
Prospector specific production -- a measure of the system's energy production per unit power per year, calculated using prospector satellite weather data
system_df -- a dataframe containing all the results from the previous two modules as well as the productions
'''


#example:
# address = "1407 Broadway, New York, NY"

# geocode_response = GoogleGeocode(parse_address(address))

# state = getStatefromJSON(geocode_response)
# formatted_address = getFormattedAddressfromJSON(geocode_response)

# prospector_specific, tmy3_specific, prospector_monthly, tmy3_monthly = calculate_prospector_and_tmy3(formatted_address, state)

# print("TMY3 Specific Production:", np.round(tmy3_specific, 2), "kWh/kW/yr")
# print("Prospector Specific Production:", np.round(prospector_specific, 2), "kWh/kW/yr")

# tmy_specific_productions = [tmy3_specific] * len(cost_and_size_df)
# prospector_specific_productions = [prospector_specific] * len(cost_and_size_df)

# #create a dataframe for the specific production
# specific_production_df = pd.DataFrame({"TMY3 Specific Production [kWh/kW/yr]": tmy_specific_productions,
#                                        "Prospector Specific Production [kWh/kW/yr]": prospector_specific_productions})

# #add the two dataframes together
# system_df = pd.concat([cost_and_size_df, specific_production_df], axis = 1)

# system_df.to_csv("System DF.csv")

