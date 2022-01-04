# flake8: noqa

import gi

gi.require_version("Plantd", "1.0")

from gi.repository import Plantd, GLib, GObject


class TestJob(Plantd.Job):
    __gtype_name__ = "TestJob"
    __gsignals__ = {"event": (GObject.SignalFlags.RUN_LAST, object, (object,))}

    def __init__(self, job_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_value = job_value

    def do_task(self):
        Plantd.debug("Your jobValue = %s" % self.job_value)
        Plantd.debug("Successfully ran the test job!")
