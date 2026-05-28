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

inputPaths = None
inputVideos = None
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

def ConvertVideos(root, getInputVideos, getInputPaths, getOutputPath, getVideoBitRate, getAudioBitRate, getFrames):
    pass

    print("Button Clicked!!\n Getting Variables...")

    global remaining
    global videos
    global app

    global inputPaths
    global inputVideos

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
    
    app = root

    # Checks to see if the following following values are valid:
    # - Bitrates & FPS
    # - Input Videos & Paths 
    # - getOutputPath Videos & Paths 
    try:

        videoBR = int(getVideoBitRate)
        audioBR = int(getAudioBitRate)
        fps = int(getFrames)
        print(f"{printSpacer}\nBitrate & FPS set!")

        inputPaths = sorted(getInputPaths)
        inputVideos = sorted(getInputVideos)
        print("Input Videos & Paths Set!")

        outputPath = getOutputPath
        outputFile = sorted(os.listdir(outputPath))
        print(f"Path Videos & Paths Set!\n{printSpacer}\n")
        
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
    
    #Checks for total videos inside 
    videos = 0
    for i in range(len(inputVideos)):
        videos += 1    



    # This code block checks if files in the Output share the same name as any of the files in the Input
    # If the user has files with the same name and wishes to not overwrite them, this knows what files to ignore.

    try:

        # Defining Variables

        global fileCopies
        global videoSkipList
        global videoSkipListPaths
        fileCopies = 0
        videoSkipList = []
        videoSkipListPaths= inputPaths.copy()

        inputMax = len(inputVideos) - 1
        outputMax = len(outputFile) - 1

        sharedNameLoop = True
        inputLoopIndex = 0
        outputLoopIndex = 0
        videoSkipTotal = videos
        videoSkipIndexes = []

        if outputMax >= 0:

            while sharedNameLoop == True: 

                print("Loop Started!!!\n")

                print(f"{printSpacer}\nInput Index: {inputLoopIndex} | getOutputPath Index: {outputLoopIndex}\nInput Max: {inputMax} | getOutputPath Max: {outputMax}\n{printSpacer}\n")

                # Starts checking if a file in Output shares a name from any files in the Input
                if inputLoopIndex <= inputMax and outputLoopIndex <= outputMax: 

                    print("Checking for shared names...\n")

                    # If one has been found, add input index to list.
                    if inputVideos[inputLoopIndex] == outputFile[outputLoopIndex]:

                        print(f"{fileCopies} shared names found! Adding index to overwrite ignore list...\nFile: {inputVideos[inputLoopIndex]}")

                        fileCopies += 1

                        videoSkipIndexes.append(inputLoopIndex)

                        inputLoopIndex += 1
                        outputLoopIndex = 0       

                    else:

                        print("File does not share a name, skipping...\n")
                        outputLoopIndex += 1

                # If current Output file does not match, add to skip list & check the next file in queue.
                elif outputLoopIndex > outputMax:
                    
                    print(f"File: {inputVideos[inputLoopIndex]} does not share a name with getOutputPath, adding to non-copy queue...\n")

                    videoSkipList.append(inputVideos[inputLoopIndex])
                    
                    inputLoopIndex += 1
                    outputLoopIndex = 0

                # Scanning Done
                else:

                    print(f"Finished!!\nThere were {fileCopies} shared names Found!\n")

                    # Get a list that copies elements from Input Path List & a variable that copies the total Input videos
                    # Pop each video index that shares a name in Output & removes set number of files from skip total.
                    for i in (range(len(videoSkipIndexes))):

                        print(f"Pop Values: {videoSkipIndexes}")
                        print(f"Non-Shared File Paths: {videoSkipListPaths}\n")
                        print(f"Current Skippable Videos: {videoSkipTotal}\n")  

                        print("Removing from video total...")
                        videoSkipTotal -= 1

                        print("popping from list...")
                        videoSkipListPaths.pop(videoSkipIndexes[i] - i)

                    sharedNameLoop = False



        if fileCopies > 0:

            print(f"{fileCopies} Copies Found!!\nTotal Videos to Skip for Override: {videoSkipTotal}")
        else:
            print("No Copies found!!")

    except Exception as e:
        ErrorHandler(e, "Failed to find files with the same name")


    print(f"Found Files: {fileCopies}\n{videoSkipList}\n\nNon-Shared Name Files: {videoSkipListPaths}")


    startConvert = messagebox.askquestion(title="Confirm?", message="Do You Want to Convert Videos?")
    
    if startConvert == "yes":

        if fileCopies > 0:

            # Warning when shared names are detected
            warningText = f"There are {fileCopies} videos that share the same name."
            if videoSkipTotal == 0:
                warningText = "All selected files share the same name."
            overwriteAnswer = messagebox.askyesnocancel(icon="warning",title="Overwrite?", message=f"{warningText}\n    Do you wish to overwrite them?\n\n           Yes: Overwrite | No: Skip")
            
            # Yes: Skip ask prompt ffmpeg gives when converting file of the same name.
            # No: Replace Videos, Paths & Total Videos from Input with values made when detecting copies, ignoring files that share names. 
            if overwriteAnswer == True:
                startArgs = "ffmpeg -y"
            elif overwriteAnswer == False:
                videos = videoSkipTotal
                inputVideos = videoSkipList
                inputPaths = videoSkipListPaths
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

        #vidioBRStr = str(videoBR)
        #audioBRStr = str(audioBR)
        #fpsStr = str(fps)

        # Adding options to a string for ffmpeg commmand
        options = f'-b:v {str(videoBR)}k -b:a {str(audioBR)}k -r {str(fps)}'

        print("Starting Thread...")
        StartFFmpeg() 
        
        # Returns these values to be used outside this function
        return remaining, videos, app, startArgs, videoBR, audioBR, fps, inputPaths, inputVideos, options, outputPath, outputFile, progressWindow, progress, ProcessingText, QueueVideoTitle, remaining


# ===========
#   Threads
# ===========

# Moves converting to new process to not affect Progress Bar Window
def StartFFmpeg():
    print("starting FFmpeg")
    threading.Thread(target=FFmpegThread).start()

def FFmpegThread():

    try:
        
        print(inputVideos[0])
        print("Thread Entered!!")
        
        # Displays current video title in Progress Bar
        QueueTitleLimit = 40
        QueueVideoTitle = inputVideos[0]
        if len(QueueVideoTitle) > QueueTitleLimit:
            QueueVideoTitle = f"{QueueVideoTitle[0:QueueTitleLimit]}..."
        ProcessingText.config(text=f"Converting: {QueueVideoTitle}")
        print("Title Entered!!")    

        # Setting up command line for loop iiteration
        finalOutput = f"{outputPath}/{inputVideos[0]}"

        ffmpeg_cmd = f'{startArgs} -i "{inputPaths[0]}" {options} "{finalOutput}"'
        
        print(ffmpeg_cmd)
        print("Command Line Set!!!")

        # Starts converting
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

    # Removes converted video
    inputPaths.pop(0)
    inputVideos.pop(0)

    # Checks if files still exist in Input list
    if inputPaths:
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