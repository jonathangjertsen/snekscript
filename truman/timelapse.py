"""
Makes a timelapse from yesterday
"""
from datetime import datetime, timedelta
from glob import glob
from os import makedirs, path
from shutil import copyfile, rmtree
from subprocess import check_output

from constant import FILE_NAME_FORMAT, JUST_DATE_FORMAT

TEMP_DIR = "temp"

if __name__ == "__main__":
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime(JUST_DATE_FORMAT)
    makedirs(TEMP_DIR, exist_ok=True)
    inputs = glob("cam-{}T*.jpg".format(yesterday))
    dates = [datetime.strptime(input_, FILE_NAME_FORMAT) for input_ in inputs]
    for i, (_, name) in enumerate(sorted(zip(dates, inputs))):
        new_name = path.join(TEMP_DIR, "cam-{:06d}.jpg".format(i))
        copyfile(name, new_name)
    check_output(["ffmpeg", "-y", "-framerate", "12", "-i", TEMP_DIR + r"/cam-%06d.jpg", "timelapse-{}.mp4".format(yesterday)])
    rmtree(TEMP_DIR)
