import os
import subprocess
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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
    # Get the duration of each video file
    durationList = []
    for video in videoList:
        duration = subprocess.Popen([resource_path('ffprobe'), '-v', 'error', '-show_entries', 'format=duration', '-of',
                                    'default=noprint_wrappers=1:nokey=1', video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        duration = duration.stdout.read().decode('utf-8')
        duration = float(duration)
        durationList.append(duration)
    # Sum up the duration of all the video files
    durationSum = 0
    for duration in durationList:
        durationSum += duration
    # Return the duration sum
    return durationSum


duration_in_seconds = videoDurationSum()
# Convert the duration to hours, minutes and seconds
hours = int(duration_in_seconds / 3600)
minutes = int((duration_in_seconds - hours * 3600) / 60)
seconds = int(duration_in_seconds - hours * 3600 - minutes * 60)
# Print the duration
print('The duration of all the videos in the current directory is:')
print(str(hours) + ' hours ' + str(minutes) +
      ' minutes ' + str(seconds) + ' seconds')
input("Enter any key to exit")
