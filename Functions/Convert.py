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



videoBR = None
audioBR = None
fps = None

outputFile = None

def ConvertVideos(root, videoCollection, videoNames, outputPath, videoBitRateInt, audioBitRateInt, framesInt):

    # Goes through all videos in folder to calculate remaining videos for Progress Bar
    
    #print(outputPath)

    try:

        videoBR = int(videoBitRateInt)
        audioBR = int(audioBitRateInt)
        fps = int(framesInt)

        print(f"{videoBR} {audioBR} {fps}")

    except ValueError:
        messagebox.showwarning(title="Option Values Not a Number", message="Please Only Use Numbers for Options")
        return
    except Exception as e:
        #messagebox.showerror(title="Unknown Error", message="Unknown Error Has Occured")
        print(e)
        return

    
    outputFile = os.listdir(outputPath)

    fileCopies = 0

    for x in range(len(outputFile)):
        for y in range(len(videoNames)):
            if outputFile[x] == videoNames[y]:
                print(f"Copy Found!\n Input File: {videoNames[y]}\n Output File: {outputFile[x]}")
                videoNames.pop()
                videoCollection.pop(y)
                fileCopies += 1
                print("Copy Found!")
            else:
                print("Not a copy. Ignoring...")

    #print(f"Paths: {videoCollection}\n, Videos: {videoNames}")


    videos = 0

    for i in range(len(videoNames)):
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

            vidBitStr = str(videoBitRateInt)
            audBitStr = str(audioBitRateInt)
            framesStr = str(framesInt)

            options = f'-b:v {vidBitStr}k -b:a {audBitStr}k -r {framesStr}'

            StartFFmpeg(progressWindow, videoCollection, videoNames, options, outputPath, progress, remaining)

            '''
            try:
                #progress['value'] += remaining
    
            except Exception as e:
                messagebox.showerror(message=e)
                root.bell()
            else:
                currentVideo.config(text="Finished!")
            '''     
                        
            
        #progressWindow.mainloop()

    else:
        messagebox.showerror(title="Folders Not Set",message="Folders Not Found, Please Setup Folder Paths.")

# ===========
#   Threads
# ===========

def StartFFmpeg(root, vidCollection, videos, options, outputPath, progress, remaining):
    threading.Thread(target=FFmpegThread, args=(root, vidCollection, videos, options, outputPath, progress, remaining)).start()


def FFmpegThread(root, vidCollection, videos, options, outputPath, progress, remaining):

    print("Thread Entered!!")

    outputVar = outputPath + "/" + videos[0]

    ffmpeg_cmd = f'ffmpeg -i "{vidCollection[0]}" {options} "{outputVar}"'
    print(ffmpeg_cmd)

    subprocess.run(ffmpeg_cmd, check=True)
    root.after(20, VideoQueue(root, vidCollection, videos, options, outputPath, progress, remaining))

def VideoQueue(root, vidCollection, videos, options, outputPath, progress, remaining):

    print("Entered Queue!!")

    print(f"Remaining: {remaining}")

    progress['value'] += remaining

    print(progress['value'])

    vidCollection.pop(0)
    videos.pop(0)

    if vidCollection and  videos:
        print("Loading Next Video...")
        FFmpegThread(root, vidCollection, videos, options, outputPath, progress, remaining)
    else:
        messagebox.showinfo(title="Conversion Successful!", message="Files Have Been Converted!")  
        root.destroy()  

'''

def StringToValue(videoBitRate, audioBitRate, frames):

    try:

        audioBitRateInt = int(audioBitRate)
        videoBitRateInt = int(videoBitRate)
        framesInt = int(frames)

        #print(f"{audioBitRateInt} {videoBitRateInt} {framesInt}")

    except ValueError:
        messagebox.showwarning(title="Option Values Not a Number", message="Please Only Use Numbers for Options")
    except Exception as e:
        #messagebox.showerror(title="Unknown Error", message="Unknown Error Has Occured")
        print(e)

    return videoBitRate, audioBitRate, frames
'''

