import os

import gi

gi.require_version("Pd", "1.0")

from gi.repository import Pd  # noqa: E402


class EventSink(Pd.Sink):
    __gtype_name__ = "EventSink"

    def __init__(self, *args, **kwargs):
        endpoint = os.getenv("PLANTD_MODULE_HUE_EVENTS_BACKEND", "tcp://localhost:12000")
        super().__init__(*args, **kwargs)
        self.set_endpoint(endpoint)
        self.set_filter("")

    def do_handle_message(self, msg):
        event = Pd.Event.new()
        if event is None:
            raise Exception("failed to create an event")
        # event.deserialize(msg)
        Pd.debug(msg)
