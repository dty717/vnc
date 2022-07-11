from tkinter import *
from tkinter import ttk
import threading
from config.config import srcIndex
from PIL import Image,ImageTk
from service.logger import Logger
import cv2


class CameraBoard(Frame):
    cameraRunning = False
    def __init__(self, master,**kargs):
        super().__init__(master,kargs)
        self.stream = cv2.VideoCapture(srcIndex)
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.panel = None
        self.pauseLoop()
        if not self.stream.isOpened():
            Logger.log("摄像异常", "当前摄像头无法打开", "设备端口"+str(srcIndex), 1200)
    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        if not self.stream.isOpened():
            return
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                if self.stream == None:
                    return
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                (grabbed, img) = self.stream.read()
                # self.frame = img
                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                image = Image.fromarray(image)
                # image = PhotoImage("img_closepressed", data=image)
                image = ImageTk.PhotoImage(image)
                # print(image)
                # # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = Label(self,image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")
    def pauseLoop(self):
        self.stopEvent.set()
    def continueLoop(self):
        self.stopEvent.clear()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)