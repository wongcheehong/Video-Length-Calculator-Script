import os
import subprocess
import sys
import re
from colorama import init
from colorama import Fore, Back


init(autoreset=True)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def natural_sort_key(s):
    _nsre = re.compile('([0-9]+)')
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def format_duration(duration):
    hours = int(duration / 3600)
    minutes = int((duration - hours * 3600) / 60)
    seconds = int(duration - hours * 3600 - minutes * 60)
    return f"{hours}h{minutes}m{seconds}s"


def watch_until_which_video(need_to_watch, start_folder="", start_video=""):
    """
    need_to_watch: time in seconds you need to watch
    start_folder: folder where you start watching
    """
    current_dir = os.getcwd()

    # Get all the subdirectories
    subdirs = [x[0] for x in os.walk(current_dir)]
    subdirs.sort(key=natural_sort_key)
    del subdirs[0]  # Does not include the current directory

    if start_folder:
        start_folder_path = os.path.abspath(start_folder)
        if not os.path.isdir(start_folder_path):
            return print("Folder not exists")
        index = subdirs.index(start_folder_path)
        subdirs = subdirs[index:]
    else:
        start_folder = subdirs[0]

    duration_sum = 0
    run_only_once = True
    for subdir in subdirs:
        # Get files in subdirs
        file_list = os.listdir(subdir)
        video_list = [file for file in file_list if file.endswith('.mp4')]
        video_list.sort(key=natural_sort_key)

        if start_video and run_only_once:
            index = video_list.index(start_video)
            video_list = video_list[index:]
            run_only_once = False
        for video in video_list:
            video_path = os.path.join(subdir, video)
            duration = subprocess.Popen([resource_path('ffprobe'), '-v', 'error', '-show_entries', 'format=duration', '-of',
                                        'default=noprint_wrappers=1:nokey=1', video_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            duration = duration.stdout.read().decode('utf-8')
            duration_sum += float(duration)
            if duration_sum >= need_to_watch:
                watch_until_folder = os.path.relpath(subdir, current_dir)
                print("Watch until this folder > " +
                      Fore.CYAN + watch_until_folder)
                print("Until this video > " + Fore.GREEN + video)
                print("You will watch " + Fore.YELLOW +
                      format_duration(duration_sum))
                return

    return print("Watch until the last video of the end folder ")


if __name__ == '__main__':
    print("Based on the duration you want to watch, this script will help you determine you should watch until which video.")
    print("Video must be numbered correctly in order for this to work.")

    need_to_watch = int(
        input("\nHow much of time you need to watch in minutes: "))

    print("\nIf you leave it empty, it will start from the first folder of current directory.")
    start_folder = input(
        "Start from which folder (Provide the exact folder name): ")
    print("\nIf you leave it empty, it will start from the first video of the specifed folder.")
    start_video = input("Start from video (example_video.mp4)> ")
    print()
    watch_until_which_video(need_to_watch*60, start_folder, start_video)
    input("Press Enter to exit")
