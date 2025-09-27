import math
import sys
import time
import json
from .load import runtime_load
import shutil

def oldrender(fps, padding):
    start = time.time()
    frames = runtime_load(fps)
    frame_count = len(frames.keys())
    for i in range(frame_count):
        last_frame = time.time()
        frame = frames[f"{i}"]
        complete_frame = ""
        width = shutil.get_terminal_size().columns
        for n in range(math.floor(padding / 2)):
            complete_frame += "\n"
        for line in frame.split("\n"):
            complete_frame += line.center(width) + "\n"
        for n in range(math.ceil(padding / 2)):
            complete_frame += "\n"
        sys.stdout.write((complete_frame + "\r"))
        while time.time() - last_frame < 1/fps:
            pass
    end = time.time()
    print(f"\nRendered {frame_count} frames in {round(end - start, 2)} seconds ({round(frame_count / (end - start), 2)} FPS)")
    return
            

def render(fps):
    frames = runtime_load(fps)
    for i in range(len(frames.keys())):
        sys.stdout.write(frames[str(i)])
    return
