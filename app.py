from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from Functions import Buttons as Btn
from Functions import Convert as Cvrt
import ctypes

window = Tk()


icon = PhotoImage(file="Images/icon.png")
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# ===============
# Variables
# ===============
mainColor = "#312E2E"
textColor = "#FFFFFF"

videoNames = None
VideoPathsList = None

# ===============
#Defining Window
# ===============
window.resizable(False, False)
window.geometry("610x360")
window.title("Video Jpeg4")
window.iconphoto(True, icon)
window.config(background=mainColor)

# ===============
# Functions
# ===============

def AddButton():

    global videoNames
    global VideoPathsList

    inputVideos = []
    inputCollection = []

    try:        

        inputCollection, inputVideos = Btn.AddVideoManager(inputCollection, inputVideos, window)    

    except TypeError:

        print("No Videos Selected Or Cancelled.\n")
        print(f"Paths: {VideoPathsList}\nVideos: {videoNames}\n")

    except Exception as e:

        Cvrt.ErrorHandler(e, "Assigning Files Failed")

    else:

        print("Inserting Videos...")
        VideoPathsList, videoNames = inputCollection, inputVideos
        VideoBoxListRefresh()
        print(f"Paths: {VideoPathsList}\nVideos: {videoNames}")
        return VideoPathsList, videoNames


def RemoveButton():

    selectedVideos = VideoTextBox.curselection()

    for videos in selectedVideos[::-1]:
        del VideoPathsList[videos]
        del videoNames[videos]
    
def VideoBoxListRefresh():

    VideoTextBox.delete(0,END)

    for video in range(len(videoNames))[::-1]:
        VideoTextBox.insert(0, videoNames[video])

def Output():

    filepath = filedialog.askdirectory(title = "Choose an Output Folder.")

    # Checks if user accepted an output folder.
    # If they cancelled, do not make textfield empty
    if filepath != "":

        try:

            outputPath.delete(0,END)
            outputPath.insert(0,filepath)

        except Exception as e:

            print(e) 
    else:
        return


def Convert():

    try:

        print(f"videoNames: {videoNames}\nVideoTextBox: {VideoTextBox.get(0, END)}\nVideoPathsList: {VideoPathsList}\n")

        Cvrt.ConvertVideos(window, VideoPathsList, videoNames, outputPath.get(), videoBitRate.get(), audioBitRate.get(), frames.get())

    except Exception as e:
        print(e)

# ===============
# Input Folder
# ===============

InputFileButton = Button(window, text="Add Videos",padx=5,command=lambda:[AddButton()]).place(x=20,y=90)
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
# Options
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

renderIterations = Spinbox(window, width=2, from_=1, to=10000)
renderIterations.place(x=470,y=40)
renderIterationsLabel = Label(window,text="Render Iterations",bg=mainColor,fg=textColor).place(x=500,y=40)

# ===============
# Export Stuff
# ===============

exportButton = Button(window, text="Start Jpeg-ifying", command=Convert, compound=TOP).place(x=488,y=90)

VideoTextBox = Listbox(window,width=93, height=13, relief="sunken",borderwidth=2,selectmode="multiple")
VideoTextBox.place(x=20,y=120)

window.mainloop()
