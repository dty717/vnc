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
        lastLocation = list(getLastLocation()); 
        if len(lastLocation) == 1:
            lastLocation = lastLocation[0]
            latitude = lastLocation['latitude']
            longitude = lastLocation['longitude']
        else:
            latitude = lat_deg
            longitude = lon_deg
        cityInfo = tkintermapview.convert_coordinates_to_city(latitude, longitude)
        if cityInfo == None:
            cityInfo = str(round(latitude,4))+","+str(round(longitude,4))
        else:
            cityInfo  = "\r\n" + str(round(latitude,4))+","+str(round(longitude,4))
        self.map_widget.set_position(latitude, longitude, marker=False)  # Berlin, Germany
        self.marker = self.map_widget.set_marker(latitude, longitude, text=cityInfo, command=self.marker_click)
    def marker_click(marker):
        print(f"marker clicked - text: {marker.text}  position: {marker.position}")


        # 
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())


# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)