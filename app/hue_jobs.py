# flake8: noqa
import os

import gi

from .hue.house import House

gi.require_version("Plantd", "1.0")

from gi.repository import GObject, Plantd


class ChangeRoomJob(Plantd.Job):
    __gtype_name__ = "SetRoomJob"
    __gsignals__ = {"event": (GObject.SignalFlags.RUN_LAST, object, (object,))}

    def __init__(self, room, properties, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.properties = properties
        self.room = room
        house_ip = os.getenv("PLANTD_MODULE_HUE_IP")
        self.house = House(house_ip)

    def do_task(self):
        if "brightness" in self.properties:
            Plantd.debug(f"setting the {self.room} brightness to {self.job_value}")
            brightness = int(self.properties["brightness"])
            try:
                self.house.set_room_brightness(self.room, brightness)
            except LookupError as e:
                Plantd.error(e)
