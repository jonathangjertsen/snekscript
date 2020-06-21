from os import path
from time import sleep
from contextlib import contextmanager

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
            sleep(preview_duration)
            self._cam.capture(location)
            self._cam.stop_preview()

    def record(self, location: str, record_duration: float, settings: dict=None):
        with camera_settings(self._cam, settings):
            self._cam.start_preview()
            self._cam.start_recording(location)
            time.sleep(record_duration)

    def try_settings(self, directory: str):
        for exposure_mode in self._cam.EXPOSURE_MODES:
            for awb_mode in self._cam.AWB_MODES:
                for brightness in range(100):
                    for contrast in range(100):
                        self.shoot(
                            location=path.join(directory, "brightness-{}_contrast-{}_exposure_mode-{}_awb_mode-{}.jpg".format(
                                brightness,
                                contrast,
                                exposure_mode,
                                awb_mode,
                            )),
                            settings={
                                "brightness": brightness,
                                "contrast": contrast,
                                "exposure_mode": exposure_mode,
                                "awb_mode": awb_mode,
                            }
                        )

if __name__ == "__main__":
    from picamera import PiCamera
    cam = RpiCamera(camera=PiCamera())
    cam.try_settings(".")
