import os
import re
from pymediainfo import MediaInfo


def get_video_duration(video_path):
    clip_info = MediaInfo.parse(video_path)
    duration_seconds = clip_info.tracks[0].duration / 1000

    return duration_seconds


def natural_sort_key(s):
    _nsre = re.compile('([0-9]+)')
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def format_duration(duration):
    hours = int(duration / 3600)
    minutes = int((duration - hours * 3600) / 60)
    seconds = int(duration - hours * 3600 - minutes * 60)

    message = ""
    if hours > 0:
        message += str(hours) + "h "
    if minutes > 0:
        message += str(minutes) + "m "
    if seconds > 0:
        message += str(seconds) + "s"
    if not message:
        message = "0s"

    return message


def videoDurationInThisPath(path):
    # Get the list of files in the current directory
    fileList = os.listdir(path)
    # Get the list of video files
    videoList = [file for file in fileList if file.endswith('.mp4')]
    # Get the duration of each video file
    durationList = []
    for video in videoList:
        video_path = os.path.join(path, video)
        duration = get_video_duration(video_path)
        durationList.append(duration)
    # Sum up the duration of all the video files
    durationSum = sum(durationList)
    # Return the duration sum
    return durationSum


# Sum up all the video duration in current directory and subdirectories
def videoDurationSumCurrentAndSubdir():
    currentDir = os.getcwd()

    # Get all the subdirectories
    subdirs = [x[0] for x in os.walk(currentDir)]
    subdirs.sort(key=natural_sort_key)

    # Get the video duration in all the subdirectories
    durationSum = 0
    for subdir in subdirs:
        duration = videoDurationInThisPath(subdir)
        relativePath = os.path.relpath(subdir, currentDir)
        print(f"{relativePath}: {format_duration(duration)}")
        durationSum += duration
    return durationSum


duration_in_seconds = videoDurationSumCurrentAndSubdir()
print('\nThe duration of all the videos in the current directory is:')
print(format_duration(duration_in_seconds))
input("Enter any key to exit")
