import os
import re
from colorama import init
from colorama import Fore
from pymediainfo import MediaInfo

init(autoreset=True)


def natural_sort_key(s):
    _nsre = re.compile('([0-9]+)')
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def get_video_duration(video_path):
    clip_info = MediaInfo.parse(video_path)
    duration_seconds = clip_info.tracks[0].duration / 1000

    return duration_seconds


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


# Sum up all the video duration in current directory
def videoDurationSum():
    # Get the current directory
    currentDir = os.getcwd()
    # Get the list of files in the current directory
    fileList = os.listdir(currentDir)
    # Get the list of video files
    videoList = []
    for file in fileList:
        if file.endswith('.mp4'):
            videoList.append(file)
    videoList.sort(key=natural_sort_key)
    # Get the duration of each video file
    durationSum = 0
    for video in videoList:
        duration = get_video_duration(video)
        durationSum += duration
        print(f"{Fore.GREEN}{video}: {Fore.YELLOW}{format_duration(duration)} {Fore.RESET}(Cumulative Sum: {Fore.CYAN}{format_duration(durationSum)}{Fore.RESET})")
    # Return the duration sum
    return durationSum


duration_in_seconds = videoDurationSum()
# Print the duration
print('\nThe duration of all the videos in the current directory is: ' + Fore.GREEN +
      format_duration(duration_in_seconds))
input("Enter any key to exit")
