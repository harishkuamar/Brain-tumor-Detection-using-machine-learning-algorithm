import tkinter
from PIL import Image
from tkinter import filedialog
import cv2 as cv
from frames import *
from displayTumor import *
from predictTumor import *
import matplotlib.pyplot as plt

class Gui:
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    val = 0
    fileName = 0
    DT = object()
    mriImage = None  # Initialize mriImage to None

    wHeight = 700
    wWidth = 1180

    def __init__(self):
        global MainWindow
        MainWindow = tkinter.Tk()
        MainWindow.geometry('1200x720')
        MainWindow.resizable(width=False, height=False)

        self.DT = DisplayTumor()

        self.fileName = tkinter.StringVar()

        self.FirstFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, 0, 0)
        self.FirstFrame.btnView['state'] = 'disable'

        self.listOfWinFrame.append(self.FirstFrame)

        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))

        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val,
                                  value=1, command=self.check)
        RB1.place(x=250, y=200)
        RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region",
                                  variable=self.val, value=2, command=self.check)
        RB2.place(x=250, y=250)

        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=8, command=self.browseWindow)
        browseBtn.place(x=800, y=550)

        # Add a back button
        back_btn = tkinter.Button(self.FirstFrame.getFrames(), text="Back", width=8, command=self.back)
        back_btn.place(x=900, y=550)

        MainWindow.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileName)
        imageName = str(self.fileName)
        mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)

    def back(self):
        # Handle the back button action here
        if len(self.listOfWinFrame) > 1:
            current_frame = self.listOfWinFrame.pop()
            current_frame.hide()
            previous_frame = self.listOfWinFrame[-1]
            previous_frame.unhide()

        if len(self.listOfWinFrame) == 1:
            self.listOfWinFrame[0].btnView['state'] = 'disable'

    def displayAccuracyGraph(self, accuracy_values):
        plt.figure(figsize=(6, 4))
        plt.plot(accuracy_values, marker='o', linestyle='-')
        plt.title('Accuracy Over Time')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.grid(True)
        plt.show()

    def applyGaussianBlur(self):
        global mriImage
        mriImage = cv.GaussianBlur(mriImage, (5, 5), 0)
        self.listOfWinFrame[0].readImage(Image.fromarray(mriImage))
        self.listOfWinFrame[0].displayImage()

    def applyCannyEdgeDetection(self):
        global mriImage
        mriImage = cv.Canny(mriImage, 100, 200)
        self.listOfWinFrame[0].readImage(Image.fromarray(mriImage))
        self.listOfWinFrame[0].displayImage()

    def check(self):
        global mriImage
        if (self.val.get() == 1):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)

            res = predictTumor(mriImage)

            if res > 0.5:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Tumor Detected", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="red")
            else:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="No Tumor", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="green")

            resLabel.place(x=700, y=450)

        elif (self.val.get() == 2):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, self.DT.displayTumor, self.DT)

            self.listOfWinFrame.append(secFrame)

            for i in range(len(self.listOfWinFrame)):
                if (i != 0):
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            if (len(self.listOfWinFrame) > 1):
                self.listOfWinFrame[0].btnView['state'] = 'active'

            accuracy_values = [0.75, 0.82, 0.88, 0.92, 0.95]  # Replace with your actual accuracy values
            self.displayAccuracyGraph(accuracy_values)

            # Add a "Gaussian Blur" button
            gaussian_blur_btn = tkinter.Button(self.FirstFrame.getFrames(), text="Apply Gaussian Blur", width=18, command=self.applyGaussianBlur)
            gaussian_blur_btn.place(x=600, y=600)

            # Add a "Canny Edge Detection" button
            canny_edge_detection_btn = tkinter.Button(self.FirstFrame.getFrames(), text="Apply Canny Edge Detection", width=25, command=self.applyCannyEdgeDetection)
            canny_edge_detection_btn.place(x=800, y=600)

        else:
            print("Not Working")

mainObj = Gui()
