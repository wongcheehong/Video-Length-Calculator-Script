import os
import re
from colorama import init
from colorama import Fore
from pymediainfo import MediaInfo


init(autoreset=True)


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
    first_time_running = True
    day = 1
    for subdir in subdirs:
        # Get files in subdirs
        file_list = os.listdir(subdir)
        video_list = [file for file in file_list if file.endswith('.mp4')]
        video_list.sort(key=natural_sort_key)

        # Run only once because start_video only exist in the starting folder
        if start_video and first_time_running:
            index = video_list.index(start_video)
            video_list = video_list[index:]
            first_time_running = False
        for video in video_list:
            video_path = os.path.join(subdir, video)
            duration = get_video_duration(video_path)
            duration_sum += duration
            if duration_sum >= need_to_watch:
                watch_until_folder = os.path.relpath(subdir, current_dir)
                print(f"\n--Day {day}--")
                print("Watch until this folder > " +
                      Fore.CYAN + watch_until_folder)
                print("Until this video > " + Fore.GREEN + video)
                print("You will watch " + Fore.YELLOW +
                      format_duration(duration_sum))
                day += 1
                duration_sum = 0

    print(f"\n--Day {day}--")
    print("Watch until the last video of the end folder ")
    print("You will watch " + Fore.YELLOW + format_duration(duration_sum))


if __name__ == '__main__':
    print("Based on the duration you want to watch, this script will help you determine you should watch until which video.")
    print("Video must be numbered correctly in order for this to work.")

    need_to_watch = int(
        input("\nHow much time you need to watch in minutes per day: "))

    print("\nIf you leave it empty, it will start from the first folder of current directory.")
    start_folder = input(
        "Start from which folder (Provide the exact folder name): ")
    print("\nIf you leave it empty, it will start from the first video of the specifed folder.")
    start_video = input("Start from video (example_video.mp4)> ")
    print()
    watch_until_which_video(need_to_watch*60, start_folder, start_video)
    input("Press Enter to exit")
