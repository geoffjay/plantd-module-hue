#!/usr/bin/env python
import json
import os
import signal
import sys
import threading

import gi
from flask import Flask

from app import App

gi.require_version("Plantd", "1.0")

from gi.repository import Plantd  # noqa: E402

web_app = Flask(__name__)


@web_app.route("/health-check")
def root():
    return json.dumps({"status": "alive"})


def run_module():
    log_file = os.getenv("PLANTD_MODULE_LOG_FILE", "/dev/null")

    Plantd.log_init(True, log_file)

    app = App()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    status = app.run(sys.argv)

    Plantd.log_shutdown()

    return status


def main():
    # make CI happy, we need a listening port to allow it to be recognized
    if not os.getenv("PLANTD_MODULE_STANDALONE", False):
        threading.Thread(
            target=web_app.run,
            args=(
                "0.0.0.0",
                5555,
            ),
        ).start()
    return run_module()


if __name__ == "__main__":
    sys.exit(main())
