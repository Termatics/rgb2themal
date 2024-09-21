from moviepy.editor import VideoFileClip
import os

def extract_frames(video_path, output_folder, fps=3):
    if fps <= 0:
        raise ValueError("fps must be a positive integer")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = VideoFileClip(video_path)
    duration = video.duration
    frame_number = 0

    # Calculate the time interval between frames in seconds
    frame_interval = 1 / fps

    # Iterate over the time points at which to extract frames
    t = 0
    while t < duration:
        frame = video.get_frame(t)
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.png")
        video.save_frame(frame_filename, t)
        frame_number += 1
        t += frame_interval

    print(f"Extracted {frame_number} frames to '{output_folder}'")



# Replace with your video file path and output directory
video_path = "path to video"
output_folder = "path to output folder"
extract_frames(video_path, output_folder, fps=3)