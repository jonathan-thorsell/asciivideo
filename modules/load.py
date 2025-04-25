
import cv2
import os
import sys
from PIL import Image
import json
import time
import math

frame_file = "frames.json"
characters = " .:-=+H%"
#characters = " ░▒▓"


def video_is_loaded():
    return os.path.exists(frame_file)

def get_frame_count():
    if not video_is_loaded():
        return 0
    with open(frame_file) as f:
        frames = json.load(f)
    return len(frames.keys())

def get_frame(frame_number):
    with open(frame_file) as f:
        frames = json.load(f)
    return frames[frame_number]

def load_ascii(video, print_frame_progression, size):
    start_time = time.time()
    cap = cv2.VideoCapture(video)
    frames_dict = {}
    frame_count = 0

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while cap.isOpened():
        # Read the next frame
        ret, frame = cap.read()
        if not ret:
            break

        # Downsize the frame while maintaining aspect ratio, making the height 40 pixels
        aspect_ratio = frame.shape[1] / frame.shape[0]
        new_height = size
        new_width = int(new_height * aspect_ratio * 2)
        frame = cv2.resize(frame, (new_width, new_height))

        # Process the frame into ASCII representation
        image = Image.fromarray(frame)
        image = image.convert("L")  # convert to grayscale
        pixels = image.load()
        ascii_frame = ""
        for i in range(image.height):
            for j in range(image.width):
                brightness = pixels[j, i]  # Get the brightness of the pixel
                index = int(brightness / 255 * len(characters))  # Get the index of the character that corresponds to the brightness
                if index >= len(characters):
                    index = len(characters) - 1
                character = characters[index]
                ascii_frame += character  # Add the character to the frame
            ascii_frame += "\n"  # Onto the next row

        frames_dict[frame_count] = ascii_frame
        frame_count += 1
        if print_frame_progression and frame_count % 10 == 0:
            elapsed_time = time.time() - start_time
            estimated_total_time = (elapsed_time / frame_count) * total_frames
            estimated_time_remaining = estimated_total_time - elapsed_time
            sys.stdout.write(f"Frame {frame_count}/{total_frames} processed | {math.ceil(frame_count / elapsed_time)} FPS | Estimated time remaining: {math.ceil(estimated_time_remaining)} seconds\n")

    cap.release()
    os.system("cls" if os.name == "nt" else "clear")
    print("Finishing up...")
    # Return the dictionary of frames and add it to frames.json
    with open("frames.json", "w") as f:
        json.dump(frames_dict, f)
    
    return frames_dict


def runtime_load(fps):
    print("Loading frames... This will only take a moment.")
    with open("frames.json") as r:
        frames = json.load(r)

    new_frames = {}
    count = 0
    for i in range(len(frames.keys())):
        for n in range(fps):
            new_frames[str(count)] = frames[f"{i}"]
            count += 1
    
    return new_frames