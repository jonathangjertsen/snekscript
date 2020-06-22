from contextlib import contextmanager
from collections import OrderedDict
import datetime
from fractions import Fraction
from os import path, utime
from time import sleep, time
from shutil import copyfile
import sys

from constant import FILE_DATE_FORMAT

RESOLUTION = (1024, 768)
RESIZED_RESOLUTION = ()

NIGHT_SETTINGS = OrderedDict([
    ("framerate", Fraction(1, 6)),
    ("shutter_speed", 6_000_000),
    ("exposure_mode", "off"),
    ("iso", 800),
    ("led", False),
    ("_pre_sleep", 10),
])
DAY_SETTINGS = {
    "exposure_mode": "auto",
    "awb_mode": "auto",
    "brightness": 50,
    "contrast": 50,
    "led": False,
    "_pre_sleep": 2,
}
NIGHT_START = (20, 0)
NIGHT_END = (8, 0)

def get_settings():
    dt = datetime.datetime.now()
    if NIGHT_END < (dt.hour, dt.minute) < NIGHT_START:
        return { **DAY_SETTINGS, "annotate_text": dt.strftime(FILE_DATE_FORMAT) }
    else:
        return { **NIGHT_SETTINGS, "annotate_text": dt.strftime(FILE_DATE_FORMAT) }

def get_driver():
    try:
        dummy = sys.argv[1] == "test"
    except IndexError:
        dummy = False

    if dummy:
        return DummyCam()
    else:
        from picamera import PiCamera
        return PiCamera()

@contextmanager
def camera_settings(camera, settings: dict=None):
    if settings is None:
        settings = {}

    backup = {}
    for key, value in settings.items():
        try:
            backup[key] = getattr(camera, key)
        except AttributeError:
            pass

        try:
            setattr(camera, key, value)
        except AttributeError:
            pass

    yield

    for key, value in backup.items():
        setattr(camera, key, value)

class DummyCam(object):
    def __init__(self):
        pass

    def __getattr__(self, key):
        return key

    def close(self):
        print("Closed")

    def start_preview(self):
        print("Started preview")

    def stop_preview(self):
        print("Stopped preview")

    def capture(self, location):
        print("Capture at location: {}".format(location))
        with open(location, "a"):
            utime(location, None)

    def start_recording(self, location):
        print("Start recording")

    def stop_recording(self, location):
        print("Stop recording")


class RpiCamera(object):
    def __init__(self, camera):
        self._cam = camera

    def shoot(self, location: str, preview_duration: float=2.0, settings: dict=None):
        with camera_settings(self._cam, settings):
            self._cam.start_preview()
            sleep(settings["_pre_sleep"])
            self._cam.capture(location)
            self._cam.stop_preview()

    def record(self, location: str, record_duration: float, settings: dict=None):
        with camera_settings(self._cam, settings):
            self._cam.start_preview()
            self._cam.start_recording(location)
            time.sleep(record_duration)
            self._cam.stop_recording()


if __name__ == "__main__":
    dt = datetime.datetime.now()
    filename = dt.strftime("cam-{}.jpg".format(FILE_DATE_FORMAT))

    print(get_settings())

    driver = get_driver()
    try:
        cam = RpiCamera(driver)
        cam.shoot(filename, settings=get_settings())
        copyfile(filename, "latest.jpg")
    finally:
        driver.close()
