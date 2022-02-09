import requests
import json

BASE_URL = "https://maps.googleapis.com/maps/api/"
GOOGLE_API_KEY = "AIzaSyARoizs3vxF0OBbTqL10Ry7be2CUtALamE"
GEOCODE_BASE_URL = BASE_URL + "geocode/json?key={}".format(GOOGLE_API_KEY)
STATICMAP_BASE_URL = BASE_URL + "staticmap?key={}".format(GOOGLE_API_KEY)

#Function to get the JSON response for a Google Geocode API request
#this API takes an address as an input and returns coordinates and other address info
def GoogleGeocode(address):
    # url = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyCOe8WdmAMkXv4e0UebQTjso0d7Wsj3PNg"
    url = GEOCODE_BASE_URL
    
    address = address.replace(" ", "+")
    url += ("&address=" + address)
    
    response = requests.get(url)
    json_response = json.loads(response.text)
    return json_response

#Functions to get site coordinates from the JSON response
def getLatfromJSON(json):
    lat = json['results'][0]['geometry']['location']['lat']
    return lat

def getLonfromJSON(json):
    lon = json['results'][0]['geometry']['location']['lng']
    return lon

def getStateandZIPfromJSON(json):
    state = ""
    zip_code = 0
    
    for level in json['results'][0]['address_components']:
        level_type = level['types'][0]
        if(level_type == "postal_code"):
            zip_code = level['long_name']
        if(level_type == "administrative_area_level_1"):
            state = level['short_name']
    
    return state, zip_code

def geocode_address(address_to_geocode):
    #geocode address to ensure validity
    google_address = GoogleGeocode(address_to_geocode)
    try:
        formatted_address = google_address['results'][0]['formatted_address']
        lat, lon = getLatfromJSON(google_address), getLonfromJSON(google_address)
        state, zip_code = getStateandZIPfromJSON(google_address)
    except:
        formatted_address = "Could not find specified address :/"
        lat, lon = 0,0
        state, zip_code = "", 0
    
    return formatted_address, lat, lon, state, zip_code

def CoordinateGeocode(coordinates):
    #geocode coordinates using Google Geocoding API
    #inputs: coordinates tuple of floats
    #outputs: api response dictionary
    # url = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyCOe8WdmAMkXv4e0UebQTjso0d7Wsj3PNg"
    url = GEOCODE_BASE_URL
    
    url += ("&latlng=" + str(coordinates[0]) + "," + str(coordinates[1]))
    
    response = requests.get(url)
    json_response = json.loads(response.text)
    
    formatted_address = json_response['results'][0]['formatted_address']
    
    return formatted_address

def static_maps_request(lat, lon, scale):
    # url = "https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyCOe8WdmAMkXv4e0UebQTjso0d7Wsj3PNg"
    URL = STATICMAP_BASE_URL
    size = '500x400'
    
    center = str(lat) + "," + str(lon)
    url += "&center="
    url += center
    
    url += "&format="
    url += "png"
    
    url += "&size="
    url += str(size)
    
    url += "&scale=" + str(scale)
    url += "&zoom=17"
    
    url += "&maptype=roadmap"
    
    url += "&style=feature:all|element:labels|visibility:off"
    url += "&style=feature:road|element:geometry|visibility:off"
    url += "&style=feature:administrative|element:all|visibility:off"
    url += "&style=feature:transit|element:all|visibility:off"
    url += "&style=feature:water|element:all|visibility:off"
    
    response = requests.get(url) #image
    
    return response, url

def static_maps_request_satellite(lat, lon, scale):
    # url = "https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyCOe8WdmAMkXv4e0UebQTjso0d7Wsj3PNg"
    url = STATICMAP_BASE_URL
    size = '500x400'
    
    center = str(lat) + "," + str(lon)
    url += "&center="
    url += center
    
    url += "&format="
    url += "png"
    
    url += "&size="
    url += str(size)
    
    url += "&scale=" + str(scale)
    url += "&zoom=17"
    
    url += "&maptype=satellite"
    
    response = requests.get(url) #image 
    
    return response, url


def retrieveGeocodeData(address, scale=1):
    formatted_address, lat, lon, state, zip_code = geocode_address(address)
    respons, url = static_maps_request_satellite(lat, lon, scale)
    image = respons.content
    return image, url, formatted_address, lat, lon, state, zip_code

#this is the function that determines which buildings belong to the address
#it works by finding the centroid of each contour (building) and then finding the coordinates of that point
#then, it inputs those coordinates into the CoordinateGeocode function which returns an address
#if that address matches the formatted version of the address input by the user (taken from the google geocode API response output)
#then we include that building, otherwise, we exclude that building
#note: the function only checks this for buildings that are 500 feet away or less, for speed's sake, but your version can change this threshold
def geocode_test(address_image, contours, formatted_address, feet_per_px, scale):
    #check if each contour is in the appropriate address
    center = (0, 0)
    cx = center[0]
    cy = center[1]
    
    #find the coordinates of the center
    json_response = GoogleGeocode(formatted_address)
    lat = getLatfromJSON(json_response)
    lon = getLonfromJSON(json_response)
    
    coordinates = "(" + str(lat) + "," + str(lon) + ")"
    
    #find all contour distances and angles from the center
    distances, angles, areas, selected_contours = [],[],[],[]
    for contour in contours:
        
        #find center point of contour
        M = cv2.moments(contour)
        px = int(M["m10"] / M["m00"])
        py = int(M["m01"] / M["m00"])
        center_original = (px, py)
        if(scale == 1):
            center_new = (px - 320, 320 - py)
        else:
            center_new = (px - 640, 640 - py)
        
        #find x and y distance
        x_dist = (cx - center_new[0]) ** 2
        y_dist = (cy - center_new[1]) ** 2
        
        #compute distance of center of image to center of contour
        distance = np.sqrt(x_dist + y_dist) * (feet_per_px)
        
        #compute slope of center of image to center of contour
        y_diff = (cy - center_new[1])
        x_diff = (cx - center_new[0])
        if(x_diff == 0):
            angle = 90
        else:
            slope = y_diff / x_diff
            angle = np.degrees(np.arctan(slope))
        
        #adjust the angle based on quadrant
        new_angle = find_quadrant(center_new, angle)
        
        #compute contour area
        area = cv2.contourArea(contour) * (feet_per_px**2)
        
        #print(final_lat, final_lon, new_address)
        
        #distances.append(np.round(distance, 1))
        #angles.append(np.round(angle, 1))
        #areas.append(np.round(area, 1))
        
        #if contour is less than 500 feet away, find its address
        if(distance < 500):
            #compute the distance in meters
            distance = distance * 0.3048

            #compute the distance in coordinates
            dx = distance * np.cos(np.radians(new_angle))
            dy = distance * np.sin(np.radians(new_angle))

            #compute the delta in coordinates
            delta_lon = dx/(111320*np.cos(np.radians(lat)))
            delta_lat = dy/110540

            #compute the final coordinates
            final_lon = lon + delta_lon
            final_lat = lat + delta_lat
            coordinates = (final_lat, final_lon)
            
            #find new address from coordinates
            new_address = CoordinateGeocode(coordinates)
            
            #draw the new address on the image
            #cv2.putText(address_image, new_address, center_original, cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)
        
            if(new_address == formatted_address):
                #fill in the contour that is within the same address
                cv2.drawContours(address_image, [contour], -1, (0, 255, 0), 2)
                areas.append(area)
                selected_contours.append(contour)
    
    return address_image, areas, selected_contours