# flake8: noqa
import gi

from .hue.house import House

gi.require_version("Plantd", "1.0")

from gi.repository import GLib, GObject, Plantd


class KitchenJob(Plantd.Job):
    __gtype_name__ = "KitchenJob"
    __gsignals__ = {"event": (GObject.SignalFlags.RUN_LAST, object, (object,))}

    def __init__(self, job_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_value = job_value
        self.room = "kitchen"

    def do_task(self):
        Plantd.debug(f"setting the {self.room} brightness to {self.job_value}")
        house = House()
        house.set_room_brightness(self.room, int(self.job_value))


class SpareBedroomJob(Plantd.Job):
    __gtype_name__ = "SpareBedroomJob"
    __gsignals__ = {"event": (GObject.SignalFlags.RUN_LAST, object, (object,))}

    def __init__(self, job_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_value = job_value
        self.room = "spare-bedroom"

    def do_task(self):
        Plantd.debug(f"setting the {self.room} brightness to {self.job_value}")
        house = House()
        house.set_room_brightness(self.room, int(self.job_value))
