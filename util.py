import os
import sys
from moviepy.editor import *
from converter import Converter
import imageio
'''def convert(word):
    print(word)
    videoClip = VideoFileClip(f"temp_files\\videos\\{word}.mp4")
    videoClip.write_gif(f"temp_files\\gifs\\{word}.gif")
    if os.path.exists(f"temp_files\\gifs\\nah.gif") != True:
        videoClip = VideoFileClip("temp_files\\videos\\nah.mp4")
        videoClip.write_gif("temp_files\\gifs\\nah.gif")
    if os.path.exists(f"temp_files\\gifs\\trans.gif") != True:
        videoClip = VideoFileClip("temp_files\\videos\\trans.mp4")
        videoClip.write_gif("temp_files\\gifs\\trans.gif")
    if os.path.exists(f"temp_files\\gifs\\near.gif") != True:
        videoClip = VideoFileClip("temp_files\\videos\\near.mp4")
        videoClip.write_gif("temp_files\\gifs\\near.gif")
'''
def merge(gif):
    gif_paths = ["temp_files\\videos\\trans.mp4", f"temp_files\\videos\\{gif}.mp4", "temp_files\\videos\\nah.mp4", "temp_files\\videos\\near.mp4"]  # Список изображени
    g1 = VideoFileClip(gif_paths[0])
    g2 = VideoFileClip(gif_paths[1])
    g3 = VideoFileClip(gif_paths[2])
    g4 = VideoFileClip(gif_paths[3])
    video = concatenate_videoclips([g1,g2,g3,g4], method="compose")
    video.write_videofile(f"temp_files\\videos\\{gif}.mp4")

'''inputpath = f"temp_files\\videos\\{gif}.mp4"
    
    outputpath = f"graph\\{gif}.gif"
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputpath, outputpath))

    reader = imageio.get_reader(inputpath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputpath, fps=fps)
    for i,im in enumerate(reader):
        sys.stdout.write("\rframe {0}".format(i))
        sys.stdout.flush()
        writer.append_data(im)
    print("\r\nFinalizing...")
    writer.close()
    print("Done.")
'''
def change_name(word):
    fullword = ""
    for let in word:
        if (let == "0"):
            fullword += 'z'
        elif (let == "1"):
            fullword += 'o'
        elif (let == "2"):
            fullword += 'tw'
        elif (let == "3"):
            fullword += 'th'
        elif (let == "4"):
            fullword += 'fo'
        elif (let == "5"):
            fullword += 'fi'
        elif (let == "6"):
            fullword += 'si'
        elif (let == "7"):
            fullword += 'se'
        elif (let == "8"):
            fullword += 'e'
        elif (let == "9"):
            fullword += 'n'
    return fullword

