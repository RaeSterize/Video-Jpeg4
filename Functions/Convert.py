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
    
    try:
        
        for x in range(len(outputFile)):
            for y in range(len(vidFiles)):
                print(f"Loop x Index: {xLoop}\nLoop y Index: {yLoop}\n")
                if outputFile[xLoop] == vidFiles[yLoop]:

                    print(f"Copy Found!\n Input File: {vidFiles[yLoop]}\nOutput File: {outputFile[xLoop]}\n")

                    vidFiles.pop(yLoop)
                    vidsWithPaths.pop(yLoop)
                    outputFile.pop(yLoop)
                    fileCopies += 1

                    xLoop = 0
                    yLoop = 0

                    print(f"Paths: {vidsWithPaths}\nInput: {vidFiles}\n Output: {outputFile}\n")

                else:
                    print("Not a copy. Ignoring...")
                    #print(f"File List  Currently: {videoNames}\n Output File: {outputFile}\n")


    except Exception as e:
        messagebox.showerror(title="Error", message=f"ERROR! Please Report the following to the Developer!\n\nDectecting Copies Failed\n:{type(e).__name__}: {e}")
    else:
        print("No Copies found!!")
                 



    
    '''
    except Exception as e:
        messagebox.showerror(title="Error", message=f"ERROR! Please Report the following to the Developer!\n\nDectecting Copies Failed\n:{type(e).__name__}: {e}")
    
    #print(f"Paths: {videoCollection}\n, Videos: {videoNames}")

    videos = 0

    for i in range(len(vidFiles)):
        videos += 1    

    print(videos)

    # Checks if Output is Valid
    if os.path.exists(outputPath):

        startConvert = messagebox.askquestion(title="Confirm?", message="Do You Want to Convert Videos?")
        
        if startConvert == "yes":

            if fileCopies > 0:
                overwriteAnswer = messagebox.askquestion(icon="warning",title="Overwrite?", message=f"There are {fileCopies} videos that share the same name.\nDo you wish to overwrite them?")
                if overwriteAnswer == "no":
                    return
        

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
            
            return remaining, videos, app, videoBR, audioBR, fps, vidsWithPaths, vidFiles, options, outputPath, outputFile, progressWindow, progress, currentVideo, remaining
                        

    

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

    print("Thread Entered!!")

    outputVar = f"{outputPath}/{vidFiles[0]}"

    ffmpeg_cmd = f'ffmpeg -i "{vidsWithPaths[0]}" {options} "{outputVar}"'
    print(ffmpeg_cmd)

    subprocess.run(ffmpeg_cmd, check=True)
    app.after(20, VideoQueue())

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

