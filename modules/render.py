import sys
import time
import json
from .load import runtime_load

def oldrender(fps):
    start = time.time()
    frames = {}
    with open(f"frames.json") as r:
        frames = json.load(r)
    frame_count = len(frames.keys())
    for i in range(frame_count):
        last_frame = time.time()
        while time.time() - last_frame < 1/fps:
            sys.stdout.write(frames[f"{i}"])
    return time.time() - start

def render(fps):
    frames = runtime_load(fps)
    for i in range(len(frames.keys())):
        sys.stdout.write(frames[str(i)])
    return
