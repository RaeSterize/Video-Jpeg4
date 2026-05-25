from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path


def VideoManager(videoCollection, videoNames, windowRoot):


    #Gets File Path & Files
    input = filedialog.askopenfilenames(title = "Choose An Output Folder.", filetypes=[("Video Files", "*.mp4 *.mov *.webm *.mkv *.flv *.avi *.wmv")])

    try:
        if input != "":

            input = windowRoot.splitlist(input)
            
            #Converts Tuple to List
            for tuple in range(len(input)):
                videoCollection.append(input[tuple])

            #Transfers Video Files to own List
            for f in videoCollection:
                fPath = Path(f)
                videoNames.append(fPath.name)

            return videoCollection, videoNames
        else:
            return
    except Exception as e:
        messagebox.showerror(title="Error", message=f"ERROR! Please Report the following to the Developer!\n\nSorting Videos Failed:\n:{type(e).__name__}: {e}")