# ISScout
## Overview
In a world of full of information accesible on the internet, databases are a key element in maintaining
and organizing info. It can be daunting and grueling to read through these massive databases, so instead
we can create algorithms or programs that can sort or locate specific pieces. In this example, we are 
filtering through the details of the position and velocity of the ISS from different countries, regions, 
and cities. We are able to find the exact details from any city that is included with the database and other
points.
# Files
Included in this repository are a Dockerfile, Makefile, app, pytest_app, and this one README. The dockerfile 
functions to creates a format for the application and other commands that will complete the process. The makefile 
will create and set up the docker container and the flask as well. The app includes the actualy script for reading
the files and it can tested by pytest. The README simply has all the instruction for how to use this repository.
## Instructions
### Data and container
#### 1)
To download the data first go to the website 'https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq' and click on XML under the title "Public Distribution File" and "XMLsightingData_citiesUSA04" for our case.
#### 2)
This should have opened two pdf files under new tabs, which we can then copy the link of and apply it to the directory. Open up a new folder in shell and paste 'wget file:///C:/Users/boliv/Downloads/XMLsightingData_citiesUSA04%20.xml' and 'wget file:///C:/Users/boliv/Downloads/ISS.OEM_J2K_EPH%20.xml'
#### 3)
Now to create a container we must first bring up the file by using 'touch Dockerfile' and input the following lines of code within the file which will not function until the next step:
```BASH
FROM python:3.9

RUN mkdir /app
RUN pip3 install --user xmltodict

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]
``` 
#### 4)
For the flask to function we must set requirements for its application, create a text file within the folder called 'emacs requirements.txt' and write the command 'Flask==2.0.3' within the file and save.
#### 5) 
Lastly we want to build the container which should be specific to your own files and username 'docker build -t <username>/<file-name>:latest .' and to push it use a similar format 'docker push <username>/<file-name>:latest'
### Pre-containerized copy
#### 1)
Pulling a pre containerized copy of a docker container is super simple, format the following command to your specific names: 'docker pull <username>/<file-name>:latest'
### Application
#### 1)
Running the script first requires the flask to be active and to do so we must run these commands on the command line(the 5000 number is based on personal server, mine is 5004):
```BASH
export FLASK_APP=app.py
export FLASK_ENV=development
flask run -p 5004
```
#### 2)
We need to open a second terminal logged in and run the command 'curl localhost:5004/data -X POST' which will allocate the data and read
```BASH
Data transferred
```
#### 3)
Now we can input any of the following commands:
```BASH
SS Sighting Location
/                                                      (GET) Information on how to interact with the application
/data                                                  (POST) Transfer data from file
Routes for Positional and Velocity Data:

/epochs                                                (GET) All Epochs in the positional data
/epochs/<epoch>                                        (GET) All information about a specific Epoch in the positional data
Routes for Sighting Data

/countries                                             (GET) All Countries from the sighting data
/countries/<country>                                   (GET) All information about a specific Country in the sighting data
/countries/<country>/regions                           (GET) All Regions associated with a given Country in the sighting data
/countries/<country>/regions/<regions>                 (GET) All information about a specific Region in the sighting data
/countries/<country>/regions/<regions>/cities          (GET) All Cities associated with a given Country and Region in the sighting data
/countries/<country>/regions/<regions>/cities/<city>   (GET) All information about a specific City in the sighting data
```
preface the '/' with 'curl localhost:5004' and it should provide the output according to the list
### Interpretation
#### 1)
From the options we have we are able to input any of the commands which each will have different coutputs, for the commands that end with a '<location>' we are receiving information specific to that name, it should look like 'curl localhost:5008/countries/Turkey/regions/None/cities/Ankara'
```BASH
  {
    "spacecraft": "ISS",
    "sighting_date": "Fri Feb 25/04:58 AM",
    "duration_minutes": "3",
    "max_elevation": "23",
    "enters": "23 above NNW",
    "exits": "10 above NNE",
    "utc_offset": "2.0",
    "utc_time": "02:58",
    "utc_date": "Feb 25, 2022"
  },
  {
    "spacecraft": "ISS",
    "sighting_date": "Sat Feb 26/04:11 AM",
    "duration_minutes": "1",
    "max_elevation": "16",
    "enters": "16 above NNE",
    "exits": "10 above NE",
    "utc_offset": "2.0",
    "utc_time": "02:11",
    "utc_date": "Feb 26, 2022"
  },
  {
    "spacecraft": "ISS",
    "sighting_date": "Sat Feb 26/05:45 AM",
    "duration_minutes": "3",
    "max_elevation": "13",
    "enters": "10 above NW",
    "exits": "10 above NNE",
    "utc_offset": "2.0",
    "utc_time": "03:45",
    "utc_date": "Feb 26, 2022"
  }
```
We can find the information we are looking for from this command as it describes the loaction we have picked
#### 2)
The options that do not have these arrows are broad and will list out the different options of countries, regions, or cities. This is where we can find the location that we can input within the arrows, example 'curl localhost:5008/countries/Turkey/regions/None/cities
```BASH
{
   "Ankara": 14
}
```
### Citations
#### 1)
Goodwin, S. (n.d.). ISS_COORDS_2022-02-13. NASA. https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml Retrieved March 17, 2022, from https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq
#### 2)
Goodwin, S. (n.d.). XMLsightingData_citiesUSA07. NASA. Retrieved March 17, 2022, from https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA04.xml
