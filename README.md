# path-planning-data-processing-dji-drone-app
An app in KIVYMD to plan paths and generate latitude and longitude values that can be uploaded to a DJI drone effortlessly for autonomous flight. Post processing screen also available to process antenna data, as well as a map to display the flight plan that was flown 

**INTRODUCTION**
This app was developed for the NRCAN Oil Spill challenge and was initially created in MATLAB.
As MATLAB is quite rigid and not deployable, we were imagining using this application on someone's phone as carrying a laptop to a test site can be streneous, a new app on a more open source, accessible software was needed.

This app is develped on KIVYMD 2.0.1 with some KIVY elements.
The main source code is in the KivyMDApp.py file. Each of the other files are helper files and graphics used in the app.

**RUNNING THE CODE**
To run the code, KIVYMD as well as any other dependencies not found when parsing the script can be downloaded using pip.
After that the app can be started by running the program. 

**UI**
Upon start up a user is met with the home screen as well as a navigation rail to the right. The user can use the rail to seamlessly navigate through the different screens of the app.
The home screen is currently blank, asides from a welcome home button.

The user can navigate to the 'Path Planning' screen icon which is the first icon on the bottom group of icons on the navigation rail.
Here the user can input latitude and longitude data for two points which would be the top left and the bottom right coordinates of an area of interest aND the height at which the drone is expected to fly. 
The user can chose the shape of the "scan" the drone is intended to fly, as well as the antenna that is being used (as it influences the proximity of the path for an ideal scan).
Upon clicking generate file, a .csv file will be generated in the directory of the application with lat, long, and altitude data that can be uploaded to a DJI drone and flown autonomously.

The user can navigate to the 'Custom Path Planning' screen icon which is the second icon on the bottom group of icons on the navigation rail.
Here the user can choose points 'free hand' on a map for points of interest that the drone must scan, enter the height, and click generate file, and the app will generate the lat, long, and altitude the drone can fly autonomously.

The user can navigate to the 'Post Processing' screen icon which is the third icon on the bottom group of icons on the navigation rail.
Here the user can choose antenna data to represent on a log graph, to determine data trends from areas of interest.
The user can also choose the dji drone log data to visually represent where the drone actually flew during the flight on the map to the right.
(In future versions, we were hoping to have the flight data and antenna data as part of one file, right now they are two).
I have not included any flight logs for privacy reasons for our development, but I will include a file that can be used to test the plotting.

**There are photos of the different screens of interest in the app in the APP Images folder**
