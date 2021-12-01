import os
import subprocess
import sys
import re


_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def format_duration(duration):
    hours = int(duration / 3600)
    minutes = int((duration - hours * 3600) / 60)
    seconds = int(duration - hours * 3600 - minutes * 60)
    return f"{hours}h{minutes}m{seconds}s"


def videoDurationInThisPath(path):
    # Get the list of files in the current directory
    fileList = os.listdir(path)
    # Get the list of video files
    videoList = [file for file in fileList if file.endswith('.mp4')]
    # Get the duration of each video file
    durationList = []
    for video in videoList:
        video_path = os.path.join(path, video)
        duration = subprocess.Popen([resource_path('ffprobe'), '-v', 'error', '-show_entries', 'format=duration', '-of',
                                     'default=noprint_wrappers=1:nokey=1', video_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        duration = duration.stdout.read().decode('utf-8')
        duration = float(duration)
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
