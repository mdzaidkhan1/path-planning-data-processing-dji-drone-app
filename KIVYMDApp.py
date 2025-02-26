import pandas as pd
from tkinter import filedialog
import tkinter as tk
import subprocess
import threading
import numpy as np

from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.graphics import Line, Color, Ellipse
from kivy.clock import Clock
from plyer.facades.gps import GPS
#populating this screen 
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.floatlayout import FloatLayout

from kivymd.uix.navigationrail import (
    MDNavigationRailItem,
    MDNavigationRail,
    MDNavigationRailFabButton,
    MDNavigationRailItemIcon,
    MDNavigationRailItemLabel,
)

#elements
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldHelperText)

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

from kivymd.uix.button import (
    MDButton, 
    MDButtonText, 
    MDExtendedFabButton, 
    MDExtendedFabButtonText)



#for the map
from kivy_garden.mapview import MapView, MapMarker, MapMarkerPopup
from kivy_garden.graph import Graph, MeshLinePlot

import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.uix.boxlayout import MDBoxLayout

#basic kivy imports
from kivy.properties import StringProperty

root=tk.Tk()
root.withdraw()
#creating demo class, ie base class

class Demo(MDApp): 

    class MainAppScreen(MDScreen):
        pass

    class PathPlanningScreen(MDScreen):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.latsList=[]
            self.snackBar = None
            self.generated_Lats=[]
            self.generated_Longs=[]
            self.height_val = 0 
            self.genMapFlag = False
            self.markers = []
            
            self.someText1 = MDExtendedFabButtonText(text=self.dropdown_text1)
            self.dropButton1=MDExtendedFabButton(pos_hint={'center_x': 0.875, 'center_y': 0.795})
            self.dropButton1.add_widget(self.someText1)
            self.dropButton1.bind(on_release=self.openMenu1)

            self.someText2 = MDExtendedFabButtonText(text=self.dropdown_text2)
            self.dropButton2 = MDExtendedFabButton(pos_hint = {'center_x': 0.525,'center_y': 0.795})
            self.dropButton2.add_widget(self.someText2)
            self.dropButton2.bind(on_release = self.openMenu2)

            self.lats = MDTextField(MDTextFieldHintText( text="Enter Lattitudes",
                                               text_color_normal="teal"),
                           MDTextFieldHelperText(text="North, South"),
                           pos_hint={
                           'center_x': 0.15, 'center_y': 0.93},
                           size_hint_x=0.25, width=100, height=50,
                            padding=10,
                            id='lats',
                            )
            self.lats.bind( focus = self.on_focus_change )

            self.longs=MDTextField( MDTextFieldHintText( text="Enter Longitudes",
                                               text_color_normal="teal"),
                            MDTextFieldHelperText(text=" West, East",)
                            ,
                          pos_hint={
                           'center_x': 0.15, 'center_y': 0.795},
                           size_hint_x=0.25, width=100, height=50,
                           padding=10,
                           id='longs')
            
            self.longs.bind(focus = self.on_focus_change )

            self.flight_height=MDTextField( MDTextFieldHintText( text="Enter Height",
                                                text_color_normal="teal"),
                           MDTextFieldHelperText(text="m"),
                           pos_hint={
                           'center_x': 0.875, 'center_y': 0.93},
                           size_hint_x=0.2, width=100, height=50,
                           id='height',
                           padding=10)
            self.flight_height.bind( focus = self.on_focus_change )

            self.mapView=MapView(zoom=17, lat=49.800442, lon=-97.127272)

            self.panel_content=MDBoxLayout(orientation="vertical",
                                pos_hint={'center_x':0.5, 'center_y':0.45},
                                size_hint_y=0.55,
                                size_hint_x=0.8, 
                                spacing=10,
                                padding=10)
            
            self.panel_content.add_widget(self.mapView)

            self.genMap= MDButton(MDButtonText( text="Plot Path",),  
                            pos_hint={'center_x': 0.35, 'center_y': 0.1},
                            on_release=self.btnfunc,
                            id='genMap'
                            )
            
            self.genFile = MDButton( MDButtonText( text="Generate File"), 
                            id="genFile",
                            pos_hint={'center_x': 0.65, 'center_y': 0.1},
                            on_release=self.btnfunc,
                            #md_bg_color=(23/255, 182/255, 230/255, 1)
                            ) 

            self.add_widget(self.dropButton1)
            self.add_widget(self.dropButton2)
            self.add_widget(self.lats)
            self.add_widget(self.longs)
            self.add_widget(self.flight_height)
            self.add_widget(self.panel_content)
            self.add_widget(self.genMap)
            self.add_widget(self.genFile)
        #Code for the drop down menu
        
        dropdown_text1=StringProperty("Choose Antenna")
        dropdown_text2=StringProperty("Choose Path Shape")

        def openMenu1(self, item):
            menuItems=[
                {
                    "text":f"Horn Antenna",
                    "on_release": lambda x=f"Horn Antenna": self.menuCallback1(x),
                } ,
                {
                    "text":f"Large PCB",
                    "on_release": lambda x=f"Large PCB": self.menuCallback1(x),
                } ,
                {
                    "text":f"Small PCB",
                    "on_release": lambda x=f"Small PCB": self.menuCallback1(x),
                }
            ]


            self.dropDownMenu1=MDDropdownMenu(caller=item, items=menuItems)
            self.dropDownMenu1.open()
    
        def menuCallback1(self, textItem):
            self.dropdown_text1=textItem
            self.someText1.text=textItem
            if self.dropDownMenu1:
                self.dropDownMenu1.dismiss()
        
        def openMenu2( self , item ):
            menuItems=[
                {
                    "text":f"Square Wave / Scanner",
                    "on_release": lambda x=f"Square Wave / Scanner": self.menuCallback2(x),
                },
                {
                    "text":f"Perimeter",
                    "on_release": lambda x=f"Perimeter": self.menuCallback2(x),
                },
                {
                    "text":f"Spiral",
                    "on_release": lambda x=f"Spiral": self.menuCallback2(x),
                }
            ]

            self.dropDownMenu2 = MDDropdownMenu( caller = item, items = menuItems )
            self.dropDownMenu2.open()
        
        def menuCallback2( self , textItem ):
            self.dropdown_text2 = textItem
            self.someText2.text = textItem
            if self.dropDownMenu2:
                self.dropDownMenu2.dismiss()



        def on_focus_change( self, instance, value ):
            if not value:
                text=instance.text
                try:
                    if instance.id == 'lats':
                        self.latsList=[ float( num ) for num in text.split( "," )]
                        if self.snackBar != None:
                            self.snackBar.dismiss()
                            self.snackBar = None
                    elif instance.id == 'longs':
                        self.longsList=[float(num) for num in text.split(",")]
                        if self.snackBar != None:
                            self.snackBar.dismiss()
                            self.snackBar = None
                    else:
                        self.height_val=float(text)
                        if self.snackBar != None:
                            self.snackBar.dismiss()
                            self.snackBar = None

                except:
                    if instance.id == 'lats':
                        self.snackBar=MDSnackbar( MDSnackbarText(text = "Invalid Latitude Values, enter in format 'North, South' ", theme_text_color= 'Error'), duration = 10, 
                                                background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()          
                    elif instance.id == 'longs':
                        self.snackBar=MDSnackbar( MDSnackbarText(text = "Invalid Longitude Values, enter in format 'West , East' ", theme_text_color= 'Error'), duration = 10, 
                                                background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()
                    else:
                        self.snackBar=MDSnackbar( MDSnackbarText(text = "Invalid Height Values, please enter a numeric value representing the flight height. Default = 5(m) ", theme_text_color= 'Error'), duration = 10,
                                                background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()
        
        def btnfunc(self, instance):

            if instance.id == 'genMap':

                self.genMapFlag = True
                if self.dropdown_text2 == 'Square Wave / Scanner':

                    diffLong = self.latsList[0] - self.latsList[1]
                    numLat = round(diffLong/1.634e-5) #needs to be replaced after I figure out the deal with the antenna
                    newLatDif=((self.latsList[1] - self.latsList[0])/numLat)
                    numPoint=numLat*2
                    latArray=np.arange(self.latsList[1], self.latsList[0], -newLatDif)
                    lats=np.linspace( self.latsList[1] , self.latsList[0], numPoint)
                    longs=np.linspace( self.longsList[0], self.longsList[1], numPoint)
                    index = np.arange(1, numPoint + 1)
                    commonIndex = index.reshape(-1, len(latArray), order='F')

                    for i in range(len(latArray)):
                        lats[commonIndex[:, i] - 1] = latArray[i]

                    indexLong = np.arange(2, numPoint)
                    sameIndex = indexLong.reshape(-1, int(len(indexLong)/2), order='F')

                    for i in range((sameIndex.shape[1])):
                        if (i % 2 == 1):
                            longs[sameIndex[:, i] - 1] = self.longsList[0]
                        else:
                            longs[sameIndex[:, i] - 1] = self.longsList[1]

                    for i in range(len(lats)):
                        marker=MapMarkerPopup(lat=float(lats[i]), lon=float(longs[i]), source='dot.drawio.png')
                        self.mapView.add_widget(marker)
                        self.markers.append(marker)
                    
                    self.generated_Lats=lats
                    self.generated_Longs=longs

                elif self.dropdown_text2 == 'Perimeter':

                    if len(self.generated_Lats) != 0 and len(self.generated_Longs) != 0:
                        del self.generated_Lats[:]
                        del self.generated_Longs[:]
                        
                    for i in range(4):
                        if i % 2 == 0:
                            self.generated_Longs.append(self.longsList[0])
                        else:
                            self.generated_Longs.append(self.longsList[1])
                        
                        if i < 2:
                            self.generated_Lats.append(self.latsList[0])
                        else:
                            self.generated_Lats.append(self.latsList[1])
                        
                        marker=MapMarkerPopup( lat = float(self.generated_Lats[i] ), lon = float( self.generated_Longs[i] ), source = 'dot.drawio.png' )
                        self.mapView.add_widget( marker )
                        self.markers.append( marker)

            if instance.id == 'genFile':

                if self.genMapFlag == True:

                    if self.height_val == 0:

                        self.altitudeList = [5]*len(self.generated_Lats)

                    else:

                        self.altitudeList=[self.height_val]*len(self.generated_Lats)

                    df = pd.DataFrame({
                        'Latitude' : self.generated_Lats,
                        'Longitude' : self.generated_Longs,
                        'Height' : self.altitudeList,
                    })

                    try:

                        output_directory = filedialog.askdirectory( title = "Choose output file directory for custom  flight plan" )
                        df.to_excel( output_directory+r'/Flight Plan.xlsx', header = False, index = False, engine = 'openpyxl' )
                        MDSnackbar( MDSnackbarText( text = "File named 'Flight Plan' generated in chosen directory!", theme_text_color= 'Primary'), duration = 5,
                                background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()
                        
                        for marker in self.markers:
                            self.mapView.remove_widget(marker)

                        self.generated_Lats = np.array([])
                        self.generated_Longs = np.array([])
                        self.altitudeList = np.array([])

                    except:

                        MDSnackbar( MDSnackbarText( text = "Ouput Directory not chosen. Click Generate file again to save current chosen points!", theme_text_color= 'Error'), duration = 5,
                                background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()
                
                else:
                        MDSnackbar( MDSnackbarText( text = "Must generate points on the Map using Plot Path before Generating File", theme_text_color= 'Error'), duration = 10,
                                background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()





    class PostProcessingScreen(MDScreen):
       
        def __init__(self, **kwargs):
            super().__init__( **kwargs)
            self.x_points=[]
            self.y_points=[]
            self.latList=[]
            self.longList=[]   
            self.altitude=[]
            self.listOfLines=[]
            self.fig, self.ax = plt.subplots()
            #self.ax.plot(self.x_points, self.y_points, marker='o', linestyle='-', color='b')
            self.ax.set_xlabel('Frequency')
            self.ax.set_ylabel('Log Magnitude')
            self.ax.set_title('VNA Data')

            canvas = FigureCanvasKivyAgg(self.fig) 

            self.graphBox=MDBoxLayout(orientation="vertical",
                                pos_hint={'center_x':0.275, 'center_y':0.45},
                                size_hint_y=0.45,
                                size_hint_x=0.4, 
                                spacing=10,
                                padding=10
                                )
           
            self.mapBox=MDBoxLayout(orientation="vertical",
                                pos_hint={'center_x':0.725, 'center_y':0.45},
                                size_hint_y=0.44,
                                size_hint_x=0.44, 
                                spacing=10,
                                padding=10)
            
            self.map_view=MapView(zoom=17, lat=49.800442, lon=-97.127272)

            self.mapBox.add_widget(self.map_view)

            self.graphBox.add_widget(canvas)
           
            self.findVNAFile=MDButton(MDButtonText( text="Find VNA Data File"), 
                            id="findVNAFile",
                            pos_hint={'center_x': 0.275, 'center_y': 0.175},
                            on_release=self.btnfunc,)
            
            self.findMapData=MDButton(MDButtonText( text="Find Flight GPS Data"), 
                            id="findGPSFile",
                            pos_hint={'center_x': 0.725, 'center_y': 0.175},
                            on_release=self.btnfunc,)

            self.averageAltitude=MDTextField(MDTextFieldHintText(text = "Average Altitude (m)"),
                                             readonly=True, multiline=False,
                                            pos_hint = {'center_x': 0.765,'center_y': 0.71},
                                            size_hint_x= 0.325,
                                            height = 50,
                                            width = 100, 
                                            cursor_color=(0, 0, 0, 0),
                                            line_color=(0, 0, 0, 0),
                                            background_color=(1, 1, 1, 0.5),
                                            )
            
            self.add_widget(self.graphBox)
            self.add_widget(self.mapBox)
            self.add_widget(self.findVNAFile)
            self.add_widget(self.findMapData)
            self.add_widget(self.averageAltitude)        
        def btnfunc(self, instamce):
            if instamce.id == 'findVNAFile':
                inputDirectory=filedialog.askopenfilename(
                    title="Choose the file with the VNA Data",
                    filetypes=[("All files", "*.*"),
                               ("Excel files", "*.xlsx;*.xls"),
                               ("CSV Files", "*.csv")])
                data=pd.read_csv(inputDirectory)
                self.x_points=data['Frequency'].tolist()
                self.y_points=data['Log Magnitude'].tolist()
                
                self.ax.clear()

                self.ax.plot(self.x_points, self.y_points, linestyle="-", color='b')
                self.ax.set_xlabel('Frequency')
                self.ax.set_ylabel('Log Magnitude')
                self.ax.set_title('VNA Data')


                canvas = FigureCanvasKivyAgg(self.fig) 
                canvas.draw()

                for widget in self.graphBox.children:
                    if isinstance(widget, FigureCanvasKivyAgg):
                        self.graphBox.remove_widget(widget)
                        break
                
                self.graphBox.add_widget(canvas)

                del self.x_points[:]
                del self.y_points[:]
            else:
                #del self.latList[:]
                #del self.longList[:]
                #del self.listOfLines[:]
                inputDirectory=filedialog.askopenfilename(
                    title="Choose the file with the Flight GPS Data",
                    filetypes=[("All files", "*.*"),
                               ("Excel files", "*.xlsx;*.xls"),
                               ("CSV Files", "*.csv")])
                data=pd.read_csv(inputDirectory, low_memory=False, skiprows=1)
                keys=data.columns.tolist()
                self.latList = data['OSD.latitude'].tolist()
                self.longList = data['OSD.longitude'].tolist()
                self.altitude = data['OSD.altitude [ft]'].tolist() 

                self.map_view.center_on(sum(self.latList)/len(self.latList), sum(self.longList)/len(self.longList))

                markers=[]
                for i in range(len(self.latList)):
                    if i%10==0:
                        marker=MapMarkerPopup(lat=self.latList[i], lon=self.longList[i], source='dot.drawio.png')
                        self.map_view.add_widget(marker)
                        markers.append(marker)
                
                """
                with self.map_view.canvas:
                    Color(1, 1, 1, 1)
                    for j in range(len(self.latList) - 1):
                        self.lines = Line(points=(self.longList[j], self.latList[j], self.longList[j+1], self.latList[j+1]), width=4)
                        self.add_widget(self.lines)
                        self.listOfLines.append(self.lines)
                        

                #Clock.schedule_interval(self.update_route_lines, 1/10)
                averageAltitude = sum(self.altitude)/len(self.altitude)* 0.3048 
                self.averageAltitude.text=f"Average Altitude: {averageAltitude:.2f} (m)"

                """
            
                averageAltitude = sum(self.altitude)/len(self.altitude)* 0.3048 
                self.averageAltitude.text=f" {averageAltitude:.2f} "

        
        def update_route_lines(self, *args):
            with self.map_view.canvas:
                Color(1,1,1,1)
                for j in range(1, len(self.latList), 1):
                    if j<len(self.listOfLines):
                        self.listOfLines[j-1].points = [self.latList[j-1], self.longList[j-1], self.latList[j], self.longList[j]]

       

    class CustomPlanningScreen(MDScreen):
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.latList=[]
            self.longList=[]
            self.markerList=[]
            self.coordinateText=""
            self.altitude=""
            self.snackbar= None
            self.custom_map=MapView( zoom=17, lat=49.800442, lon=-97.127272, pos_hint={'center_x': 0.5,'center_y': 0.45}, size_hint={0.8, 0.55})

            self.go_button=MDButton( MDButtonText( text= "Go"),
                                    id="goButton",
                                    pos_hint = {'center_x': 0.42,'center_y': 0.8},
                                    width= 50, height = 50,
                                    on_release=self.btnfunc)

            self.genCustom=MDButton( MDButtonText( text="Generate File"), 
                            id="genFile",
                            pos_hint={'center_x': 0.5, 'center_y': 0.135},
                            on_release=self.btnfunc)
            self.enterLocation=MDTextField( MDTextFieldHintText( text="Enter Location",
                                               text_color_normal="teal"),
                            MDTextFieldHelperText(text=" Lat, Long",)
                            ,
                            id='location',
                            pos_hint={
                           'center_x': 0.22, 'center_y': 0.8},
                           size_hint_x=0.25, width=100, height=50,
                           padding=10)
            
            self.enterLocation.bind(focus = self.on_text_change)

            self.altitudeEnter=MDTextField( MDTextFieldHintText( text="Enter Height",
                                               text_color_normal="teal"),
                            MDTextFieldHelperText(text="meters",),
                            id='altitude',
                            pos_hint={
                           'center_x': 0.8, 'center_y': 0.8},
                            size_hint_x=0.2,
                            width=0.5, height=0.5,
                           padding=10)
            
            self.altitudeEnter.bind(focus=self.on_focus_change)

            self.add_widget(self.enterLocation)
            self.add_widget(self.custom_map)
            self.add_widget(self.genCustom)
            self.add_widget(self.go_button)
            self.add_widget(self.altitudeEnter)

        def on_touch_up(self, touch):
            if (touch.y > self.custom_map.y and touch.y < self.custom_map.top) and \
           (touch.x > self.custom_map.x and touch.x < self.custom_map.right) and \
            touch.button=="left" or touch.grab_current==self.custom_map:
        
            # Calculate coordinates relative to MapView
                x_in_mapview = touch.x - self.custom_map.x - 80
                y_in_mapview = touch.y - self.custom_map.y - 9

            # Get latitude and longitude at the calculated coordina tes
                lat, lon = self.custom_map.get_latlon_at(x_in_mapview, y_in_mapview)

            # Create and add MapMarkerPopup 
                dist = MapMarkerPopup(lat=lat, lon=lon, source='me_32.png')
                self.custom_map.add_widget(dist)
                self.markerList.append(dist)
                self.latList.append(lat)
                self.longList.append(lon)
        
        def btnfunc(self, instance):
            if instance.id=='genFile':
                if self.altitude != '':
                    self.altitudeList=[float(self.altitude)]*len(self.latList)
                else:
                    self.altitudeList=[5]*len(self.latList) #default 5 meters if nothing is entered.
                df=pd.DataFrame({
                    'Latitude': self.latList,
                    'Longitude':self.longList,
                    'Altitude':self.altitudeList,
                })
                try:
                    output_directory=filedialog.askdirectory(title="Choose output file directory for custom  flight plan")
                    df.to_excel(output_directory+r'/CustomFlightPlan.xlsx', header=False, index=False, engine='openpyxl')
                    MDSnackbar( MDSnackbarText( text = "File named 'Custom Flight Plan' generated in chosen directory!", theme_text_color= 'Primary'), duration = 5,
                                background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()
                    #subprocess.Popen(['explorer', output_directory]) 
                    for marker in self.markerList:
                        self.custom_map.remove_widget(marker)
                    del self.latList[:]
                    del self.longList[:]
                    del self.altitudeList[:]
                except:
                    MDSnackbar( MDSnackbarText( text = "Ouput Directory not chosen. Click Generate file again to save current chosen points!", theme_text_color= 'Error'), duration = 5,
                               background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()
                
            else:
                if self.coordinateText != '':
                    try:
                        self.custom_map.center_on(float(self.coordinateText.split(',')[0]), float(self.coordinateText.split(',')[1]))
                        if self.snackbar != None:
                            self.snackbar.dismiss()
                            self.snackbar = None
                    except:
                        self.snackbar = MDSnackbar(MDSnackbarText( text= "Invalid Coordinates, Enter in format 'Lat, Long' ", theme_text_color = 'Error'), duration = 10,
                                                    background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()

        
        def on_text_change(self, instance, text):
            if instance.id=='location':
                self.coordinateText = instance.text
            else:
                self.altitude = instance.text

        def on_focus_change( self, instance, value ):
            if not value:
                self.altitude = instance.text
                try:
                    float(self.altitude)
                    if self.snackbar != None:
                        self.snackbar.dismiss()
                        self.snackbar = None
                except:
                    if self.altitude != '':
                        self.snackbar = MDSnackbar( MDSnackbarText( text= "Invalid Height Value, Enter numeric value in meters ", theme_text_color = 'Error' ), duration = 10,
                                                   background_color = self.parent.parent.theme_cls.primary_paletteKeyColorColor).open()


    class CommonNavigationRailItem(MDNavigationRailItem):

        #Code for navigation rail items, looks like we have to include the on text and on icon functions if we want the widgets to show up.
        text = StringProperty()
        icon = StringProperty()

        
        def on_icon(self, instance, value):
            def on_icon(*ars):
                self.add_widget(MDNavigationRailItemIcon(icon=value))
            Clock.schedule_once(on_icon)

        def on_text(self, instance, value):
            def on_text(*ars):
                self.add_widget(MDNavigationRailItemLabel(text=value))
            Clock.schedule_once(on_text)   

        #Trying to add functionality in terms of opening the gps in the general vicinity of where the device is currently.
        #Encountering some problems using the pyler library in context of the current OS
        """ 
        def on_start(self):
        GPS.configure( on_location=self.on_location)
        GPS.start( minTime=1000, minDistance=1)

        def on_location(self, **kwargs):
        latitude=kwargs.get("lat")
        longitude=kwargs.get("lon")
        altitude=kwargs.get("altitude")
        print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}")
        """


    def build(self):

        #General code
        self.theme_cls.theme_style= "Light"
        self.theme_cls.primary_palette="Teal" 

        self.sm=ScreenManager()  
        homeScreen=MDScreen(name="main", md_bg_color=self.theme_cls.surfaceColor)
        pathScreen = self.PathPlanningScreen(name="path_planning", md_bg_color=self.theme_cls.surfaceColor)
        postScreen=self.PostProcessingScreen(name="post_processing" ,md_bg_color=self.theme_cls.surfaceColor)
        customScreen=self.CustomPlanningScreen(name="custom_planning", md_bg_color=self.theme_cls.surfaceColor)

        self.sm.add_widget(homeScreen)
        self.sm.add_widget(pathScreen)
        self.sm.add_widget(postScreen)
        self.sm.add_widget(customScreen)

        #Navigation Rail Code
        navLayout=MDBoxLayout(MDNavigationRail(
                MDNavigationRailFabButton(
                    icon="home",
                    on_release=self.go_home
                ),
                self.CommonNavigationRailItem(
                    icon="map",
                    text="Path Planning",
                    on_release=self.go_path

                ),
                self.CommonNavigationRailItem(
                    icon="button-pointer",
                    text="Custom Path Planning",
                    on_release=self.go_custom
                ),
                self.CommonNavigationRailItem(
                    icon="graph",
                    text="Post Processing",
                    on_release=self.post_process,
                ),
                type="selected",
                #anchor="top",  
                )
            )
        
        navLayout.add_widget(self.sm)
    
        #Home screen code

        homeButton=MDButton(MDButtonText(text="Welcome home",
                                         ),
                                         pos_hint={"center_x":0.5, "center_y": 0.5})
        
        homeScreen.add_widget(homeButton)

        #Path Planning Screen Code 

        #Layout for the Path Planning screen, doesn't help too much in terms of not letting things move around when the shape of the window
        #is changed as was the initial hope. Can probably delete this later.
        screenLayout= RelativeLayout()

        # defining Text field with all the parameters
        
    
        # defining Button with all the parameters
       
        

        
        
        # adding widgets to screen
        #screenLayout.add_widget(lats)
        #screenLayout.add_widget(longs)
        #screenLayout.add_widget(genFile)
        #screenLayout.add_widget(height)
        #screenLayout.add_widget(genMap)
        #screenLayout.add_widget(panel_content)
        #screenLayout.add_widget(dropButton)
        pathScreen.add_widget(screenLayout)

        return navLayout
 
    # defining a btnfun() for the button to
    # call when clicked on it
    def btnfunc(self, obj):
        #Dummy currently
        #We want this code to do different things based on which button is pressed
        if obj.id=="genFile":
            print("Generate File button is pressed!!")
        """ elif obj.id=="genPath":
            lat1, lat2= lats.conent.split """
    
    def on_text_change(self, instance, value):
        print("Text entered:", value)
            
    
    def go_home(self, instance):
        self.sm.current="main"
        print("Button pressed")
    
    def go_path(self, instance):
        self.sm.current="path_planning"
        print("Path processing button pressed")

    def post_process(self, instance):
        self.sm.current="post_processing"
    
    def go_custom(self, instance):
        self.sm.current="custom_planning"
    
   

 
if __name__ == "__main__":
    Demo().run()