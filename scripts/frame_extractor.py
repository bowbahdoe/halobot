# Extracts the frames from the given raw_video file and puts
# them in a corresponding folder of unlabeled frames
# https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames

import cv2
import os

from tqdm import tqdm


filename = input("Name of the video file in the raw_video directory: ")
video_path = os.path.join("./data/raw_video", filename)
video = cv2.VideoCapture(video_path)

if not os.path.exists(video_path):
    raise SystemError(f"""The specified video file cannot be found.
    Please double check the path from which this script
    is called and the path provided. Was expecting a video
    at {video_path}""")

output_path = f"./data/unlabeled_frames/{filename}"
if not os.path.exists(output_path):
    os.makedirs(output_path)

frame_number = 0

max_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
progress_bar = tqdm(range(max_frames)).__iter__()

while video.isOpened():
    success, frame = video.read()

    if not success:
        break

    cv2.imwrite(f"{output_path}/{frame_number}.png", frame)
    frame_number += 1
    next(progress_bar)

video.release()
