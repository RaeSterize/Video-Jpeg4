from tkinter import *
from tkinter import filedialog
import ctypes

from Functions import Buttons as Btn
from Functions import Convert as Cvrt


window = Tk()

icon = PhotoImage(file="icon.png")
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# ===============
# Variables
# ===============
mainColor = "#312E2E"
textColor = "#FFFFFF"

# ===============
#Defining Window
# ===============
window.geometry("610x360")
window.title("Rae's Video Crappifier")
window.iconphoto(True, icon)
window.config(background=mainColor)


# ===============
# Functions
# ===============


def AddButton():

    global videoNames
    global videoCollection

    videoNames = []
    videoCollection = []

    videoCollection, videoNames = Btn.VideoManager(videoCollection, videoNames, window, True)


def RemoveButton():

    selectedVideos = videoList.curselection()

    for videos in selectedVideos[::-1]:
        del videoCollection[videos]
        del videoNames[videos]
    
def VideoBoxListRefresh():

    videoList.delete(0,END)
    
    for video in range(len(videoNames))[::-1]:
        videoList.insert(0, videoNames[video])

    #print(videoCollection, videoNames)

def Output():

    filepath = filedialog.askdirectory(title = "Choose an Output Folder.")

    if filepath != "":  
        try:
            outputPath.delete(0,END)
            outputPath.insert(0,filepath)

        except Exception as e:
            print(e) 


def Convert():

    try:

        #videoNum, audioNum, framesNum = Cvrt.StringToValue(videoBitRate.get(), audioBitRate.get(), frames.get())

        Cvrt.ConvertVideos(window, videoCollection, videoNames, outputPath.get(), videoBitRate.get(), audioBitRate.get(), frames.get())

    except Exception as e:
        print(e)

# ===============
# Input Folder
# ===============

InputFileButton = Button(window, text="Add Videos",padx=5,command=lambda:[AddButton(), VideoBoxListRefresh()]).place(x=20,y=90)
RemoveFileButton = Button(window, text="Remove Videos",padx=5, command=lambda:[RemoveButton(), VideoBoxListRefresh()]).place(x=105,y=90)

# ===============
# Output Folder
# ===============
OuputLabel = Label(window, text="Output Path:",bg=mainColor, fg=textColor).grid(row=1,column=0,padx=5, pady=5)

OutputFilebutton = Button(window, text="Open Folder",padx=5, command=Output).grid(row = 1, column= 1, pady=5)

outputPath = Entry(window, width = 70)
outputPath.config(bd=2,relief="sunken")
outputPath.grid(row=1,column=2,padx=2, pady=5)


# ===============
# Options & Export Button
# ===============

videoBitRate = Spinbox(window, width=7, from_=1, to=10000)
videoBitRate.place(x=15,y=40)
videoBitRateLabel = Label(window,text="Video Bitrate (kbps)",bg=mainColor,fg=textColor).place(x=74,y=40)

audioBitRate = Spinbox(window,width=7, from_=1, to=10000)
audioBitRate.place(x=190,y=40)
audioBitRateLabel = Label(window,text="Audio Bitrate (kbps)",bg=mainColor,fg=textColor).place(x=250,y=40)


frames = Spinbox(window, width=4, from_=1, to=10000)
frames.place(x=370,y=40)
framesLabel = Label(window,text="Frames",bg=mainColor,fg=textColor).place(x=413,y=40)

exportButton = Button(window, text="Commence Enshitification", command=Convert, compound=TOP).place(x=435,y=90)

videoList = Listbox(window,width=93, height=13, relief="sunken",borderwidth=2,selectmode="multiple")
videoList.place(x=20,y=120)

window.mainloop()
