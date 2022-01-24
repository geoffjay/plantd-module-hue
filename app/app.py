import os

import gi

gi.require_version("Pd", "1.0")

from gi.repository import Pd  # noqa: E402

from .event_sink import EventSink
from .jobs import ChangeRoomJob


class App(Pd.Application):
    __gtype_name__ = "App"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.plantd.dev.Hue", flags=0, **kwargs)
        # load environment
        service = os.getenv("PLANTD_MODULE_SERVICE", "dev-hue")
        endpoint = os.getenv("PLANTD_MODULE_ENDPOINT", "tcp://localhost:5555")
        source_endpoint = os.getenv("PLANTD_MODULE_HUE_EVENTS_FRONTEND", "tcp://localhost:11005")
        # configure application
        self.set_endpoint(endpoint)
        self.set_service(service)
        self.set_inactivity_timeout(10000)
        # setup events
        self.event_source = Pd.Source.new(source_endpoint, "")
        self.add_source("event", self.event_source)
        self.event_sink = EventSink()
        # start things
        self.event_source.start()
        self.event_sink.start()

    def do_get_property(self, key):
        """Handle the get-property request by returning a made up value.

        :param key: the property to retrieve
        :return: `Pd.PropertyResponse`
        """
        Pd.info(f"get-property: {key}")
        response = Pd.PropertyResponse.new()
        prop = Pd.Property.new(key, "test")
        response.set_property(prop)
        return response

    def do_get_status(self):
        Pd.debug("get-status")
        response = Pd.StatusResponse.new()
        return response

    def do_submit_job(self, job_name, job_value, job_properties):
        """Handle the submit-job request"""
        response = Pd.JobResponse.new()
        if job_name == "change-room":
            job = ChangeRoomJob(job_value, job_properties)
            event = Pd.Event.new_full(1000, "change-room", f"{job_value}")
            self.send_event(event)
            response.set_job(job)
        else:
            pass
        return response
