from tkinter import *
from tkinter import ttk
import tkintermapview
from components.groupLabelButton import GroupLabelButton
from components.labelButton import SwitchLabelButton
from database.mongodb import getLastLocation
from PIL import Image
from config.config import lat_deg,lon_deg

class LocationBoard(Frame):
    cameraRunning = False
    def __init__(self, master,**kargs):
        super().__init__(master,kargs)
        # create map widget
        self.map_widget = tkintermapview.TkinterMapView(self, width=1000, height=700, corner_radius=0)
        # self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
        self.map_widget.pack(fill="both", expand=True)
        lastLocation = list(getLastLocation())
        if len(lastLocation) == 1:
            lastLocation = lastLocation[0]
            latitude = lastLocation['latitude']
            longitude = lastLocation['longitude']
        else:
            latitude = lat_deg
            longitude = lon_deg
        cityInfo = tkintermapview.convert_coordinates_to_city(latitude, longitude)
        if cityInfo != None:
            cityInfo += "\r\n"
        else:
            cityInfo = ""
        if latitude > 0:
            cityInfo += str(round(latitude,4)) +"E, "
        else:
            cityInfo += str(round(-latitude,4)) +"W, "
        if longitude > 0:
            cityInfo += str(round(longitude,4)) +"N"
        else:
            cityInfo += str(round(-longitude,4)) +"S"
        self.map_widget.set_position(latitude, longitude, marker=False)  # Berlin, Germany
        self.marker = self.map_widget.set_marker(latitude, longitude, text=cityInfo, command=self.marker_click)
    def marker_click(self,marker):
        print(f"marker clicked - text: {marker.text}  position: {marker.position}")
    def refreshPage(self):
        lastLocation = list(getLastLocation())
        if len(lastLocation) == 1:
            lastLocation = lastLocation[0]
            latitude = lastLocation['latitude']
            longitude = lastLocation['longitude']
        else:
            latitude = lat_deg
            longitude = lon_deg
        self.marker.set_position(latitude, longitude)  # change position
        (lastLatitude, lastLongitude) = self.map_widget.get_position()
        distance = (lastLongitude - longitude)*(lastLongitude - longitude) +  (lastLatitude - latitude)*(lastLatitude - latitude)            
        if distance < 1e-8:
            return
        zoom =  self.map_widget.zoom
        if distance >= 1e-6  * 10 ** (17-zoom):
            self.map_widget.set_position(latitude, longitude, marker=False)  # Berlin, Germany
        # 
        # 
        cityInfo = tkintermapview.convert_coordinates_to_city(latitude, longitude)
        if cityInfo != None:
            cityInfo += "\r\n"
        else:
            cityInfo = ""
        if latitude > 0:
            cityInfo += str(round(latitude,4)) +"E, "
        else:
            cityInfo += str(round(-latitude,4)) +"W, "
        if longitude > 0:
            cityInfo += str(round(longitude,4)) +"N"
        else:
            cityInfo += str(round(-longitude,4)) +"S"
        # 
        # cityInfo += '\r\n' 'distance:' + str(round(distance,10)) + 'zoom:' + str(zoom)
        # cityInfo += '\r\n' 'True'
        self.marker.set_text(cityInfo)  # set new text
        return
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())

# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)