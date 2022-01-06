import os

import gi

gi.require_version("Plantd", "1.0")

from gi.repository import Plantd  # noqa: E402


class EventSink(Plantd.Sink):
    __gtype_name__ = "EventSink"

    def __init__(self, *args, **kwargs):
        endpoint = os.getenv("PLANTD_MODULE_HUE_EVENTS_BACKEND", "tcp://localhost:12000")
        super().__init__(*args, **kwargs)
        self.set_endpoint(endpoint)
        self.set_filter("")

    def do_handle_message(self, msg):
        event = Plantd.Event.new()
        if event is None:
            raise Exception("failed to create an event")
        # event.deserialize(msg)
        Plantd.debug(msg)
