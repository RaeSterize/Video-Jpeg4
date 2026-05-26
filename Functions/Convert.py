from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import threading

# Variables
remaining = 0
videos = 0

# Main Window
app = None 

startArgs = "ffmpeg"

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
ProcessingText = None
QueueVideoTitle = "..."
remaining = None

def ConvertVideos(root, videoCollection, videoNames, output, videoBitRateInt, audioBitRateInt, framesInt):

    print("Button Clicked!!\n Getting Variables...")

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
    global ProcessingText
    global QueueVideoTitle
    global remaining

    app = root

    # Checks to see if the following following values are valid:
    # - Bitrates & FPS
    # - Input Videos & Paths 
    # - Output Videos & Paths 
    try:

        videoBR = int(videoBitRateInt)
        audioBR = int(audioBitRateInt)
        fps = int(framesInt)
        print("Bitrate & FPS set!")

        vidsWithPaths = sorted(videoCollection)
        vidFiles = sorted(videoNames)
        print("Input Videos & Paths Set!")

        outputPath = output
        outputFile = sorted(os.listdir(outputPath))
        print("Output Videos & Paths Set!")
        
    except TypeError:
        ErrorHandler("No Videos Added")
        return
    except FileNotFoundError:
        ErrorHandler("Output Path Has Not Been Set or Does not Exist")
        return
        #messagebox.showwarning(title="Error", message=f"Output Path Has Not Been Set or Does not Exist")
    except ValueError:
        #messagebox.showwarning(title="Option Values Not a Number", message="Please Only Use Numbers for Options")
        ErrorHandler("Please Only Use Numbers for Options")
        return
    except Exception as e:
        ErrorHandler(e)
        return
    
    
    videos = 0

    print("Checking Total Videos...")

    for i in range(len(vidFiles)):
        videos += 1    
    
    fileCopies = 0
    inputLoop = 0
    outputLoop = 0


    # Checking for Video Copies
    try:

        global loopInputPath
        global loopVids

        loopInputPath = vidsWithPaths.copy()
        loopVids = vidFiles.copy()
        loopOutputVids = outputFile.copy()
        loopNonCopyRemainder = videos

        # While logged videos from Output is not empty, run this code
        while loopOutputVids: 

            print("Loop Started!!!\n")
            
            print(f"Videos in Output: {loopOutputVids}\n")
            print(f"Index from Loop: {loopVids[inputLoop]}")
            print(f"Index from Loop: {loopVids[inputLoop]}")
            print(f"Index from Output: {loopOutputVids[outputLoop]}")

            print("Getting List Lengths...")
            inputMax = len(loopVids)
            outputMax = len(loopOutputVids)
            print(f"Input: {outputLoop}\nOutput: {inputLoop}\n")

            print("Checking for copies...\n")
            if loopOutputVids[outputLoop] == loopVids[inputLoop]:

                    print(f"Copy Found!\nInput File: {loopVids[inputLoop]}\nOutput File: {loopOutputVids[outputLoop]}\n")
                    print("Popping elements...\n")
                    # Look into making it so it adds to a list instead
                    # This removes the temporary variables & makes it so if all videos are copies in the output,
                    # they will override the whole folder instead of doing nothing due to list being empty
                    loopVids.pop(inputLoop)
                    loopInputPath.pop(inputLoop)
                    loopOutputVids.pop(outputLoop)


                    fileCopies += 1
                    print(f"Copies found: {fileCopies}\n")

                    print(f"Resetting Loops...\nInput: {outputLoop}\nOutput: {inputLoop}\nRemoving video from total videos...\n")
                    outputLoop = 0
                    inputLoop = 0
                    loopNonCopyRemainder -= 1
            else:
                print("Not a copy, skipping...")
                print("Increasing Input Loop...\n")
                inputLoop += 1

                if inputLoop > inputMax:
                    print("Resetting Inner Input...\nIncreasing Output Loop...")
                    inputLoop = 0
                    outputLoop += 1
                elif outputLoop > outputMax:
                    print("Resetting output Input...")
                    outputLoop = 0

        if fileCopies > 0:
            print(f"{fileCopies} Copies Found!!")
        else:
            print("No Copies found!!")

    except Exception as e:
        ErrorHandler(e)

    print(f"{vidFiles}\n{vidsWithPaths}")

    print(f"Videos in Input Folder: {videos}")
    print(f"Copied Files found: {loopNonCopyRemainder}")

    print(f"Videos from Loop: {loopVids}")


    startConvert = messagebox.askquestion(title="Confirm?", message="Do You Want to Convert Videos?")
    
    if startConvert == "yes":

        #startArgs = "ffmpeg"

        if fileCopies > 0:

            warningText = f"There are {fileCopies} videos that share the same name."
            if loopNonCopyRemainder == 0:
                warningText = "All selected files share the same name."

            overwriteAnswer = messagebox.askyesnocancel(icon="warning",title="Overwrite?", message=f"{warningText}\nDo you wish to overwrite them?")
            
            if overwriteAnswer == True:
                startArgs = "ffmpeg -y"
            elif overwriteAnswer == False:
                videos = loopNonCopyRemainder
                vidFiles = loopVids
                vidsWithPaths = loopInputPath
                if videos == 0:
                    return


    
        # Progress Bar Window Creation
        progressWindow = Toplevel()
        #progressWindow.update()
        progressWindow.geometry("350x90")
        progress = ttk.Progressbar(progressWindow, orient=HORIZONTAL, length=300, mode="determinate")
        progress.place(x=20, y=50)
        ProcessingText = Label(progressWindow,text=f"Converting: {QueueVideoTitle}")
        ProcessingText.place(x=20, y=18)
        
        remaining = 100 / videos
        print(f"Remaining: {remaining}")

        vidioBRStr = str(videoBR)
        audioBRStr = str(audioBR)
        fpsStr = str(fps)

        options = f'-b:v {vidioBRStr}k -b:a {audioBRStr}k -r {fpsStr}'

        print("Starting Thread...")
        StartFFmpeg() 
        
        return remaining, videos, app, startArgs, videoBR, audioBR, fps, vidsWithPaths, vidFiles, options, outputPath, outputFile, progressWindow, progress, ProcessingText, QueueVideoTitle, remaining

# ===========
#   Threads
# ===========

def StartFFmpeg():
    print("starting FFmpeg")
    threading.Thread(target=FFmpegThread).start()

def FFmpegThread():

    QueueTitleLimit = 40

    try:
        print("Thread Entered!!")
        
        QueueVideoTitle = vidFiles[0]
        if len(QueueVideoTitle) > QueueTitleLimit:
            QueueVideoTitle = f"{QueueVideoTitle[0:QueueTitleLimit]}..."

        ProcessingText.config(text=f"Converting: {QueueVideoTitle}")

        outputVar = f"{outputPath}/{vidFiles[0]}"

        ffmpeg_cmd = f'{startArgs} -i "{vidsWithPaths[0]}" {options} "{outputVar}"'
        print(ffmpeg_cmd)

        subprocess.run(ffmpeg_cmd, check=True)
        app.after(20, VideoQueue())
    except Exception as e:
        ErrorHandler(e)
        print(f"{type(e).__name__}: {e}")


def VideoQueue():

    print("Entered Queue!!")

    print("Adding to Progress Bar...")
    progress['value'] += remaining

    print(f"Video Progress: {int(progress['value'])}%")

    vidsWithPaths.pop(0)
    vidFiles.pop(0)

    if vidsWithPaths:# and  videos:
        print("Loading Next Video...")
        FFmpegThread()
    else:
        ProcessingText.config(text=f"Converting Complete!")
        messagebox.showinfo(title="Conversion Successful!", message="Files Have Been Converted!")  
        progressWindow.destroy()  

def ErrorHandler(e):
    if e == "e":
        messagebox.showerror(title="Error", message=f"ERROR! Please Report the following to the Developer!\n{type(e).__name__}: {e}")
    else:
        messagebox.showwarning(title="Error", message=f"{e}")