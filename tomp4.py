import os, time, sys
import shutil, glob
from mutagen.mp3 import MP3
###### Rerender container

work_path = os.getcwd()
processed_dir = work_path + "\\processed\\"

def check():
    mp3 = 0
    ass = 0
    for filename in os.listdir(work_path):
        if (filename.endswith(".mp3")):
            mp3 += 1
            # print( filename )
            mp3list.append(filename)
        else:
            continue
    
    for filename1 in os.listdir(work_path):
        if (filename1.endswith(".ass")):
            # print( filename1 )
            ass += 1
            asslist.append(filename1)
        else:
            continue

    if (mp3 != ass):
        print("No MP4 files in the working directory, quitting ")
        quit()
    else:
        print(str(mp3) + " mp3 and " + str(ass) + " ass files detected, Starting.")


def init_job():
    if os.path.exists(processed_dir):
        print("History cache detected, cleaning.")
        shutil.rmtree(processed_dir)
        os.makedirs(processed_dir)
        print('"processed" folder created successfully!')
        print("Videos processing will start after 5 seconds.")
    else:
        os.makedirs(processed_dir)
        print('"processed" folder created successfully!')
        print("Videos processing will start after 5 seconds.")
    time.sleep(5)

def tomp4(img, mp3list):
    rtcode = 0
    for x in range(len(mp3list)):
        audio = MP3(mp3list[x])
        bitrate = str(int(audio.info.bitrate))
        rtcode = os.system("ffmpeg -loop 1 -framerate 1 -i " + '"' + img + '"' +" -i " + '"' + mp3list[x] + '"' + " -c:v libx264 -c:a aac -b:a " + bitrate + " -shortest " + '"' + processed_dir + str(mp3list[x])[:-4] + '.mp4"')
        # print("ffmpeg -loop 1 -framerate 1 -i " + '"' + img + '"' +" -i " + '"' + mp3list[x] + '"' + " -c:v libx264 -c:a aac -b:a " + bitrate + " -shortest " + '"' + processed_dir + str(mp3list[x])[:-4] + '.mp4"')
    if rtcode != 0:
        print("Re-render failed, quitting!")
        quit()
    else:
        print("All mp3 files has been re-rendered to mp4 file with selected image.")

def insrsub(asslist):
    for filename in os.listdir(processed_dir):
        if (filename.endswith(".mp4")):
            mp4list.append(filename)
        else:
            continue
    print(mp4list)

    rtcode = 0
    for x in range(len(asslist)):
        rtcode = os.system("ffmpeg -i " + '"' + processed_dir + mp4list[x] + '"' + " -vf ass=" + '"' + asslist[x] + '"' + " " + '"' + mp4list[x] + '"')
        # print("ffmpeg -i " + '"' + processed_dir + mp4list[x] + '"' + " -vf ass=" + '"' + asslist[x] + '"' + " " + '"' + mp4list[x] + '"')
    if (rtcode != 0 ):
        print("Inserting subtitles failed, quitting!")
        quit()
    else:
        print("All subtitles inserted, operation succeed!")
    

if __name__ == "__main__":
    img = sys.argv[1]
    mp3list = []
    asslist = []
    mp4list = []
    check()
    print(mp3list)
    print(asslist)
    print(mp4list)
    init_job()
    tomp4(img, mp3list)
    insrsub(asslist)