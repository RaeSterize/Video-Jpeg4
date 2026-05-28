from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import threading

# Variables
remaining = 0
videos = 0
printSpacer = "====================================="

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

videoSkipList = None
videoSkipListPaths = None

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

    global vidsWithPaths
    global vidFiles

    global startArgs
    global videoBR
    global audioBR
    global fps
    global options
    
    global outputPath
    global outputFile

    global videoSkipList
    global videoSkipListPaths

    global progressWindow
    global progress
    global ProcessingText
    global QueueVideoTitle
    global remaining
    
    print(f"Inside function:\n {videoNames}\n {videoCollection}")


    app = root

    # Checks to see if the following following values are valid:
    # - Bitrates & FPS
    # - Input Videos & Paths 
    # - Output Videos & Paths 
    try:

        videoBR = int(videoBitRateInt)
        audioBR = int(audioBitRateInt)
        fps = int(framesInt)
        print(f"{printSpacer}\nBitrate & FPS set!")

        vidsWithPaths = sorted(videoCollection)
        vidFiles = sorted(videoNames)
        print("Input Videos & Paths Set!")

        outputPath = output
        outputFile = sorted(os.listdir(outputPath))
        print(f"Output Videos & Paths Set!\n{printSpacer}\n")
        
    except TypeError:
        ErrorHandler("", "No Videos Added")
        return
    except FileNotFoundError:
        ErrorHandler("", "Output Path Has Not Been Set or Does not Exist")
        return
    except ValueError:
        ErrorHandler("", "Please Only Use Numbers for Options")
        return
    except Exception as e:
        ErrorHandler(e, "Failed to retrieve values")
        return
    
    
    videos = 0

    print("Checking Total Videos...\n")

    for i in range(len(vidFiles)):
        videos += 1    

    # Checking for Video Copies
    try:

        sharedNameLoop = True

        global fileCopies
        global videoSkipList
        global videoSkipListPaths
        fileCopies = 0
        videoSkipList = []
        videoSkipListPaths= vidsWithPaths.copy()

        videoSkipIndexes = []

        inputMax = len(vidFiles) - 1
        outputMax = len(outputFile) - 1

        #if outputMax < 0:
            #outputMax = 0

        inputLoopIndex = 0
        outputLoopIndex = 0

        videosSkipTotal = videos
        
        print(f"{vidFiles}\n{vidsWithPaths}")

        # While logged videos from Output is not empty, run this code
        if outputMax >= 0:
            while sharedNameLoop == True: 

                print("Loop Started!!!\n")

                print(f"{printSpacer}\nInput Index: {inputLoopIndex} | Output Index: {outputLoopIndex}\nInput Max: {inputMax} | Output Max: {outputMax}\n{printSpacer}\n")

                # If all files have not been scanned.
                if inputLoopIndex <= inputMax and outputLoopIndex <= outputMax: 

                    print("Checking for shared names...\n")

                    # If copy found, add to ignore list to avoid
                    if vidFiles[inputLoopIndex] == outputFile[outputLoopIndex]:

                        print(f"{fileCopies} shared names found! Adding current file to overwrite ignore list...\nFile: {vidFiles[inputLoopIndex]}")

                        fileCopies += 1

                        videoSkipIndexes.append(inputLoopIndex)

                        inputLoopIndex += 1
                        outputLoopIndex = 0       

                    else:

                        print("File does not share a name, skipping...\n")
                        outputLoopIndex += 1

                # If current Output File does not match.
                elif outputLoopIndex > outputMax:
                    
                    print(f"File: {vidFiles[inputLoopIndex]} does not share a name with output, adding to non-copy queue...\n")

                    videoSkipList.append(vidFiles[inputLoopIndex])
                    
                    inputLoopIndex += 1
                    outputLoopIndex = 0

                #Scanning Done
                else:

                    print(f"Finished!!\nThere were {fileCopies} shared names Found!\n")

                                

                    #Removes same name videos from list when asked to ignore copies.
                    for i in (range(len(videoSkipIndexes))):

                        print(f"Pop Values: {videoSkipIndexes}")
                        print(f"Non-Shared File Paths: {videoSkipListPaths}\n")
                        print(f"Current Skippable Videos: {videosSkipTotal}\n")  


                        print("Removing video from non-copy list")
                        videosSkipTotal -= 1

                        print("popping...")
                        videoSkipListPaths.pop(videoSkipIndexes[i] - i)

                    sharedNameLoop = False



        if fileCopies > 0:

            print(f"{fileCopies} Copies Found!!\nTotal Videos to Skip for Override: {videosSkipTotal}")
        else:
            print("No Copies found!!")

    except Exception as e:
        ErrorHandler(e, "Failed to find files with the same name")


    print(f"Found Files: {fileCopies}\n{videoSkipList}\n\nNon-Shared Name Files: {videoSkipListPaths}")


    startConvert = messagebox.askquestion(title="Confirm?", message="Do You Want to Convert Videos?")
    
    if startConvert == "yes":

        #startArgs = "ffmpeg"

        if fileCopies > 0:

            warningText = f"There are {fileCopies} videos that share the same name."
            if videosSkipTotal == 0:
                warningText = "All selected files share the same name."

            overwriteAnswer = messagebox.askyesnocancel(icon="warning",title="Overwrite?", message=f"{warningText}\n    Do you wish to overwrite them?\n\n           Yes: Overwrite | No: Skip")
            
            if overwriteAnswer == True:
                startArgs = "ffmpeg -y"
            elif overwriteAnswer == False:
                videos = videosSkipTotal
                vidFiles = videoSkipList
                vidsWithPaths = videoSkipListPaths
                if videos == 0:
                    return
            else:
                return


    
        # Progress Bar Window Creation
        progressWindow = Toplevel()
        progressWindow.resizable(False, False)
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
        
        print(vidFiles[0])
        print("Thread Entered!!")
        
        
        QueueVideoTitle = vidFiles[0]
        if len(QueueVideoTitle) > QueueTitleLimit:
            QueueVideoTitle = f"{QueueVideoTitle[0:QueueTitleLimit]}..."
        ProcessingText.config(text=f"Converting: {QueueVideoTitle}")
        print("Title Entered!!")    

        outputVar = f"{outputPath}/{vidFiles[0]}"

        print("Conversion Starting...")    
        ffmpeg_cmd = f'{startArgs} -i "{vidsWithPaths[0]}" {options} "{outputVar}"'
        print(ffmpeg_cmd)
        print("Command Line Set!!!")

        subprocess.run(ffmpeg_cmd, check=True)
        app.after(20, VideoQueue())
        print("Conversion Finished!")
    except Exception as e:
        ErrorHandler(e, "Conversion has failed")
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

def ErrorHandler(e, errorMessage):
    if e != "":
        messagebox.showerror(title="Error", message=f"ERROR! Please Report the following to the Developer!{errorMessage}: {type(e).__name__}: {e}")
    else:
        messagebox.showwarning(title="Error", message=f"{errorMessage}")