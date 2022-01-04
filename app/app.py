import os

import gi

from .event_sink import EventSink
from .test_job import TestJob

gi.require_version("Plantd", "1.0")

from gi.repository import Plantd  # noqa: E402


class App(Plantd.Application):
    __gtype_name__ = "App"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.plantd.dev.Hue", flags=0, **kwargs)
        # load environment
        service = os.getenv("PLANTD_MODULE_SERVICE", "dev-hue")
        endpoint = os.getenv("PLANTD_MODULE_ENDPOINT", "tcp://localhost:5555")
        source_endpoint = os.getenv("TEST_EVENTS_FRONTEND", "tcp://localhost:11005")
        # configure application
        self.set_endpoint(endpoint)
        self.set_service(service)
        self.set_inactivity_timeout(10000)
        # setup events
        self.event_source = Plantd.Source.new(source_endpoint, "")
        self.add_source("event", self.event_source)
        self.event_sink = EventSink()
        # start things
        self.event_source.start()
        self.event_sink.start()

    def do_get_property(self, key):
        """Handle the get-property request by returning a made up value.

        :param key: the property to retrieve
        :return: `Plantd.PropertyResponse`
        """
        Plantd.info(f"get-property: {key}")
        response = Plantd.PropertyResponse.new()
        prop = Plantd.Property.new(key, "test")
        response.set_property(prop)
        return response

    def do_get_status(self):
        Plantd.debug("get-status")
        response = Plantd.StatusResponse.new()
        return response

    def do_submit_job(self, job_name, job_value, job_properties):
        """Handle the submit-job request"""
        Plantd.info(f"submit-job: {job_name} [{job_value}]")
        response = Plantd.JobResponse.new()
        # for our "test" job just pass the job_value to the TestJob class
        if job_name == "test":
            job = TestJob(job_value)
            # job.connect("event", self.on_publish_event)
            event = Plantd.Event.new_full(1000, "foo", "foo-bar-baz")
            self.send_event(event)
            response.set_job(job)
        else:
            pass
        return response
