from contextlib import contextmanager
import datetime
from fractions import Fraction
from os import path, utime
from time import sleep, time
from shutil import copyfile
import sys

RESOLUTION = (1024, 768)
RESIZED_RESOLUTION = ()

NIGHT_SETTINGS = {
    "shutter_speed": 6_000_000,
    "exposure_mode": "off",
    "awb_mode": "auto",
    "iso": 800,
    "framerate": Fraction(1, 6),
    "led": False,
    "_pre_sleep": 10,
}
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
        return DAY_SETTINGS
    else:
        return NIGHT_SETTINGS

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
    temp_attributes = []
    for key, value in settings.items():
        try:
            backup[key] = getattr(camera, key)
        except KeyError:
            temp_attributes.append(key)
        setattr(camera, key, value)

    yield

    for key, value in backup.items():
        setattr(camera, key, value)

    for key in temp_attributes:
        delattr(camera, key)

class DummyCam(object):
    def __init__(self):
        pass

    def __getattr__(self, key):
        return key

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

    def settings(self, settings: dict):
        backup = {}
        for key, value in settings.items():
            backup[key] = getattr(self._cam, key)
            setattr(self._cam, key, value)
        return backup

    def shoot(self, location: str, preview_duration: float=2.0, settings: dict=None):
        with camera_settings(self._cam, settings):
            self._cam.start_preview()
            print(self._cam._pre_sleep)
            sleep(self._cam._pre_sleep)
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
    filename = dt.strftime("cam-%Y-%m-%dT%H-%M-%S.jpg")

    cam = RpiCamera(get_driver())
    cam.settings(get_settings())
    cam.shoot(filename)
    copyfile(filename, "latest.jpg")