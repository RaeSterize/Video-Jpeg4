from tkinter import *
#from tkinter import ttk
#from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
#import subprocess
#import ctypes
#import os
#import shlex
#import time
#from PIL import ImageTk, Image

def VideoManager(videoCollection, videoNames, windowRoot, saveVideo):


    #Gets File Path & Files
    input = filedialog.askopenfilenames(title = "Choose An Output Folder.", filetypes=[("Video Files", "*.mp4 *.mov *.webm *.mkv *.flv *.avi *.wmv")])

    input = windowRoot.splitlist(input)
    
    #Converts Tuple to List
    for tuple in range(len(input)):
        videoCollection.append(input[tuple])

    #Transfers Video Files to own List
    for f in videoCollection:
        fPath = Path(f)
        videoNames.append(fPath.name)

    return videoCollection, videoNames#