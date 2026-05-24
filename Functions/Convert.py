from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import threading
import time

# Variables
remaining = 0
videos = 0

# Main Window
app = None 

startArgs = None

videoBR = None
audioBR = None
fps = None

vidsWithPaths = None
vidFiles = None
options = None

outputPath = None
outputFile = None

progressWindow = None
progress = None
currentVideo = None
remaining = None

def ConvertVideos(root, videoCollection, videoNames, output, videoBitRateInt, audioBitRateInt, framesInt):

    global remaining
    global videos
    global app

    global startArgs
    global videoBR
    global audioBR
    global fps
    global vidsWithPaths
    global vidFiles
    global options
    global outputPath
    global outputFile

    global progressWindow
    global progress
    global currentVideo
    global remaining

    try:

        videoBR = int(videoBitRateInt)
        audioBR = int(audioBitRateInt)
        fps = int(framesInt)


    except ValueError:
        messagebox.showwarning(title="Option Values Not a Number", message="Please Only Use Numbers for Options")
        return
    except Exception as e:
        #messagebox.showerror(title="Unknown Error", message="Unknown Error Has Occured")
        messagebox.showerror(title="Error", message=f"ERROR! Please Report the following to the Developer!\n\n:{type(e).__name__}")
        print(e)
        return
    
    print("Test 1")

    app = root

    vidsWithPaths = sorted(videoCollection)
    vidFiles = sorted(videoNames)

    outputPath = output
    outputFile = sorted(os.listdir(outputPath))

    fileCopies = 0
    print("Test 2")
    
    xLoop = 0
    yLoop = 0
    
    print(f"{vidFiles}\n{vidsWithPaths}")

    videos = 0

    for i in range(len(vidFiles)):
        videos += 1    
    
    try:

        loopInputPath = vidsWithPaths.copy()
        loopVids = vidFiles.copy()
        loopOutputVids = outputFile.copy()

        for x in range(len(loopOutputVids)):
            for y in range(len(loopVids)):
                print(f"Loop X Index: {xLoop}\nLoop Y Index: {yLoop}\n")
                if loopOutputVids[xLoop] == loopVids[yLoop]:

                    #print(f"Copy Found!\n Input File: {loopVids[yLoop]}\nOutput File: {loopOutputVids[xLoop]}\n")

                    loopVids.pop(yLoop)
                    loopInputPath.pop(yLoop)
                    loopOutputVids.pop(yLoop)
                    fileCopies += 1

                    xLoop = 0
                    yLoop = 0

                    videos -= 1

                    #print(f"Paths: {loopInputPath}\nInput: {loopVids}\n Output: {loopOutputVids}\n")

                else:
                    pass
                    #print("Not a copy. Ignoring...")
                    #print(f"File List  Currently: {videoNames}\n Output File: {outputFile}\n")

        if fileCopies > 0:
            print(f"{fileCopies} Copies Found!!")
        else:
            print("No Copies found!!")
                    
    except Exception as e:
        messagebox.showerror(title="Error", message=f"ERROR! Please Report the following to the Developer!\n\nDectecting Copies Failed\n:{type(e).__name__}: {e}")

    '''

    print(f"{vidFiles}\n{vidsWithPaths}")


    print(videos)

    # Checks if Output is Valid
    if os.path.exists(outputPath):

        startConvert = messagebox.askquestion(title="Confirm?", message="Do You Want to Convert Videos?")
        
        if startConvert == "yes":

            startArgs = "ffmpeg"

            if fileCopies > 0:
                
                overwriteAnswer = messagebox.askyesnocancel(icon="warning",title="Overwrite?", message=f"There are {fileCopies} videos that share the same name.\nDo you wish to overwrite them?")
                
                if overwriteAnswer == True:
                    startArgs = "ffmpeg -y"
                elif overwriteAnswer == False:
                    startArgs = "ffmpeg -d"

            if videos <= 0:
                return

            print(startArgs)
        
            progressWindow = Toplevel()

            progressWindow.update()
            progressWindow.geometry("350x90")

            progress = ttk.Progressbar(progressWindow, orient=HORIZONTAL, length=300, mode="determinate")
            progress.place(x=20, y=50)


            currentVideo = Label(progressWindow,text="Processing: ")
            currentVideo.place(x=20, y=18)
            
            remaining = 100 / videos
            print(f"Remaining: {remaining}")

            vidioBRStr = str(videoBR)
            audioBRStr = str(audioBR)
            fpsStr = str(fps)

            options = f'-b:v {vidioBRStr}k -b:a {audioBRStr}k -r {fpsStr}'

 
            StartFFmpeg() 
            
            return remaining, videos, app, startArgs, videoBR, audioBR, fps, vidsWithPaths, vidFiles, options, outputPath, outputFile, progressWindow, progress, currentVideo, remaining
              

    

    else:
        messagebox.showerror(title="Folders Not Set",message="Folders Not Found, Please Setup Folder Paths.")

    '''
    

# ===========
#   Threads
# ===========

def StartFFmpeg():
    print("Starting Thread...")
    threading.Thread(target=FFmpegThread).start()

def FFmpegThread():

    try:
        print("Thread Entered!!")

        outputVar = f"{outputPath}/{vidFiles[0]}"

        ffmpeg_cmd = f'{startArgs} -i "{vidsWithPaths[0]}" {options} "{outputVar}"'
        print(ffmpeg_cmd)

        subprocess.run(ffmpeg_cmd, check=True)
        app.after(20, VideoQueue())
    except Exception as e:
        messagebox.showerror(title="Error", message=f"ERROR! Please Report the following to the Developer!\n\nDectecting Copies Failed\n:{type(e).__name__}: {e}")


def VideoQueue():

    print("Entered Queue!!")

    progress['value'] += remaining

    print(progress['value'])

    vidsWithPaths.pop(0)
    vidFiles.pop(0)

    if vidsWithPaths and  videos:
        print("Loading Next Video...")
        FFmpegThread()
    else:
        messagebox.showinfo(title="Conversion Successful!", message="Files Have Been Converted!")  
        progressWindow.destroy()  