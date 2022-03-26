from flask import Flask
import xmltodict 
import json
import logging

"""
This script works to read the information from a file and put it in pieces as specified by the commands,
it works in a flask system in order to remain as a server and stay updated. The actual program is simple
json functions to read the file, the complexity comes from the flask background that works as routes.
"""

app = Flask(__name__)

@app.route('/help', methods=['GET'])
def ask_help():
    """
    This path outputs the instructions and descriptions for the flask paths

    Args: N/A

    Returns: Returns a string 'Describe' accumulated from many strings
    """

    logging.info("Instructions for each route is being displayed")
    describe = "ISS Sighting Location\n"
    describe += "/                                                      (GET) Information on how to interact with the application \n"
    describe += "/data                                                  (POST) Transfer data from file\n"
    describe += "Routes for Positional and Velocity Data:\n\n"
    describe += "/epochs                                                (GET) All Epochs in the positional data\n"
    describe += "/epochs/<epoch>                                        (GET) All information about a specific Epoch in the positional data\n"
    describe += "Routes for Sighting Data\n\n"
    describe += "/countries                                             (GET) All Countries from the sighting data\n"
    describe += "/countries/<country>                                   (GET) All information about a specific Country in the sighting data\n"
    describe += "/countries/<country>/regions                           (GET) All Regions associated with a given Country in the sighting data\n"
    describe += "/countries/<country>/regions/<regions>                 (GET) All information about a specific Region in the sighting data\n"
    describe += "/countries/<country>/regions/<regions>/cities          (GET) All Cities associated with a given Country and Region in the sighting data\n"
    describe += "/countries/<country>/regions/<regions>/cities/<city>   (GET) All information about a specific City in the sighting data\n"
    return describe

ISS_Epoch_Data = {}
ISS_Sighting_Data = {}

@app.route('/data', methods=['POST'])
def data_into_dict():
    """
    This path reads the data and refreshes the information used for the following paths

    Args: N/A

    Returns: Returns a string confirming the file was read, the actual program opens and saves the file
    """

    logging.info("Data gathered")
    global ISS_Epoch_Data
    global ISS_Sighting_Data

    with open('ISS.OEM_J2K_EPH.xml' , 'r') as f:
        ISS_Epoch_Data =  xmltodict.parse(f.read())

    with open('XMLsightingData_citiesINT04.xml' , 'r') as f:
        ISS_Sighting_Data = xmltodict.parse(f.read())

    return f'Data transferred\n'

@app.route('/epochs', methods=['GET'])
def all_Epochs():
    """
    This path reads the file and outputs the different epochs

    Args: N/A
    
    Returns: Puts all the different epochs into a single variable and returns it as a string
    """
    logging.info("Gathering all EPOCHS...")
    EPOCH = ""
    for i in range(len(ISS_Epoch_Data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        EPOCH = EPOCH + ISS_Epoch_Data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH'] + '\n'
    return EPOCH

@app.route('/<epoch>', methods=['GET'])
def specific_Epoch(epoch: str):
    """
    This path takes in a specific epoch value and displays the details from within the file

    Args: epoch = the name of any epoch within the file in order to read its information

    Returns: Returns a dictionary of details from the specifc epoch such as velocity and position
    """
    logging.info("Gathering information on EPOCH:/"+epoch)
    Epoch_count = 0
    for i in range(len(ISS_Epoch_Data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        if epoch == ISS_Epoch_Data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH']:
            Epoch_count = i
            break
    posistion_velocity = ['X', 'Y', 'Z', 'X*', 'Y*', 'Z*']
    Epoch_dict = {}
    for vals in position_velocity:
        Epoch_dict[vals] = ISS_Epoch_Data['ndm']['oem']['body']['segment']['data']['stateVector'][Epoch_count][vals]
    return Epoch_dict

@app.route('/countries',methods=['GET'])
def all_Countries():
    """
    This path outputs all the different countries contained within the file as options

    Args: N/A

    Returns: Puts all the countries into a single variable and returns it as a string
    """
    logging.info("Gathering all countries...")
    COUNTRIES = {}
    for i in range(len(ISS_Sighting_Data['visible_passes']['visible_pass'])):
        spec_country = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['country']
        if spec_country in COUNTRIES:
            COUNTRIES[spec_country] += 1
        else:
            COUNTRIES[spec_country] = 1
    return COUNTRIES

@app.route('/countries/<country>', methods=['GET'])
def specific_Country(country):
    """
    This path takes a specific country value and displays the details from within the file

    Args: country = the name of any country within the file in order to read its information

    Returns: Returns a list of strings containing the details of the country such as its regions and cities
    """
    logging.info("Gathering info on /"+country)
    list_of_countries = []
    list_country_data = ['region', 'city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(ISS_Sighting_Data['visible_passes']['visible_pass'])):
        spec_country = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['country']
        if country == spec_country:
            country_dict = {}
            for j in list_country_data:
                country_dict[j] = ISS_Sighting_Data['visible_passes']['visible_pass'][i][j]
            list_of_countries.append(country_dict)
    return json.dumps(list_of_countries, indent=2)

@app.route('/countries/<country>/regions',methods=['GET'])
def all_Regions(country):
    """
    This path outputs all the different regions contained within the file as options

    Args: country = the name of any country within the file in order to read its information

    Returns: Puts all the regions into a single variable and returns it as a string
    """
    logging.info("Gathering all regions in /"+country)
    REGIONS = {}
    for i in range(len(ISS_Sighting_Data['visible_passes']['visible_pass'])):
        spec_country = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['country']
        if country == spec_country:
            spec_region = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['region']
            if spec_region in REGIONS:
                REGIONS[spec_region] += 1
            else:
                REGIONS[spec_region] = 1
    return REGIONS

@app.route('/countries/<country>/regions/<regions>',methods=['GET'])
def specific_Region(country, regions):
    """
    This path takes a specific country and region then displays the details from within the file

    Args: country = the name of any country within the file in order to read its information
          regions = the name of any region within the file in order to read its information

    Returns: Returns a list of strings containing the details of the region such as its cities
    """
    logging.info("Gathering info on /"+regions)
    list_of_regions = []
    list_region_data = ['city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters',\
'exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(ISS_Sighting_Data['visible_passes']['visible_pass'])):
        spec_country = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['country']
        if country == spec_country:
            spec_region = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['region']
            if regions == spec_region:
                region_dict = {}
                for j in list_region_data:
                    region_dict[j] = ISS_Sighting_Data['visible_passes']['visible_pass'][i][j]
                list_of_regions.append(region_dict)
    return json.dumps(list_of_regions, indent=2)

@app.route('/countries/<country>/regions/<regions>/cities',methods=['GET'])
def all_cities(country, regions):
    """
    This path outputs all the different cities contained within the file as options

    Args: country = the name of any country within the file in order to read its information
          regions = the name of any region within the file in order to read its information

    Returns: Returns all the cities into a single variable and returns it as a string
    """
    logging.info("Gathering all cities in /"+regions)
    CITIES = {}
    for i in range(len(ISS_Sighting_Data['visible_passes']['visible_pass'])):
        spec_country = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['country']
        if country == spec_country:
            spec_region = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['region']
            if regions == spec_region:
                spec_cities = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['city']
                if spec_cities in CITIES:
                    CITIES[spec_cities] +=1
                else:
                    CITIES[spec_cities]=1
    return CITIES

@app.route('/countries/<country>/regions/<regions>/cities/<cities>',methods=['GET'])
def specific_City(country, regions, cities):
    """
    This path takes a specific country, region, and city then displays the details from within the file

    Args: country = the name of any country within the file in order to read its information
          regions = the name of any region within the file in order to read its information
          cities = the name of any city within the file in order to read its information

    Returns: Returns a list of strings containing the details of the city such as the position and velocity
    """
    logging.info("Gathering info on /"+cities)
    list_of_cities = []
    list_city_data = ['spacecraft', 'sighting_date','duration_minutes','max_elevation','enters',\
'exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(ISS_Sighting_Data['visible_passes']['visible_pass'])):
        spec_country = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['country']
        if country == spec_country:
            spec_region = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['region']
            if regions == spec_region:
                spec_city = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['city']
                if cities == spec_city:
                    city_dict = {}
                    for j in list_city_data:
                        city_dict[j] = ISS_Sighting_Data['visible_passes']['visible_pass'][i][j]
                    list_of_cities.append(city_dict)
    return json.dumps(list_of_cities, indent=2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


