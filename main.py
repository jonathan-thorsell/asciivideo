from PIL import Image
import os
import json
import time

from modules.load import video_is_loaded, get_frame, get_frame_count, load_ascii
from modules.render import render

#### OPTIONS ####
with open('config.json') as r:
    config = json.load(r)

downsize_factor = config["downscale_factor"]
video = config["video_path"]
fps = int(1750 / (config["frame_rate"]*(4/3)))
size = config["size"]

timeit = config["time_it"]

print_frame_progression = config["print_frame_progression"]
#################
if video_is_loaded() and input("There's already a video loaded. Do you want to load a new one? (y/n): ").lower() == "y":
    available_videos = [f for f in os.listdir(video) if f.endswith(".mp4")]
    os.system("cls")
    print("Available videos:")
    for i, v in enumerate(available_videos):
        print(f"{i+1}: {v}")
    video = os.path.join(video, available_videos[int(input("Enter the number of the video you want to load: "))-1])
    load_ascii(video, print_frame_progression, size)
elif not video_is_loaded():
    print("Loading video...")
    load_ascii(video, print_frame_progression, size)
frame_count = get_frame_count()
# SHOW THE FIRST FRAME TO ADJUST THE SCREEN SIZE
first_frame = get_frame("0")
first_frame_height = first_frame.count("\n")
first_frame_width = first_frame.index("\n")
os.system("cls")
for i in range(first_frame_height):
    for n in range(first_frame_width):
        print("@", end="")
    print()
input()
# RENDER THE VIDEO
start_time = time.time()
render(fps)
if timeit:
    os.system("cls")
    for n in range(int(first_frame_height/2)):
        print()
    print(f"Rendering of {frame_count} frames took {time.time() - start_time} seconds.".center(first_frame_width))
    print(f"avg. {frame_count / (time.time() - start_time)} frames per second.".center(first_frame_width))
    for n in range(int(first_frame_height/2.5)):
        print()
    input()