#!/usr/bin/env python
import json
import os
import signal
import sys
import threading

import gi
from flask import Flask

from app import App

gi.require_version("Pd", "1.0")

from gi.repository import Pd  # noqa: E402

web_app = Flask(__name__)


@web_app.route("/health-check")
def root():
    return json.dumps({"status": "alive"})


@web_app.route("/increase-loglevel")
def increase_loglevel():
    Pd.log_increase_verbosity()
    return json.dumps({"logging": "level increased"})


@web_app.route("/decrease-loglevel")
def decrease_loglevel():
    Pd.log_decrease_verbosity()
    return json.dumps({"logging": "level decreased"})


def main():
    log_file = os.getenv("PLANTD_MODULE_LOG_FILE", "/dev/null")

    Pd.log_init(True, log_file)
    Pd.debug("starting module")

    # make CI happy, we need a listening port to allow it to be recognized
    if os.getenv("PLANTD_MODULE_STANDALONE", False) == "false":
        Pd.debug("launching web app")
        threading.Thread(
            target=web_app.run,
            args=(
                "0.0.0.0",
                5555,
            ),
        ).start()

    app = App()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    status = app.run(sys.argv)

    Pd.log_shutdown()

    return status


if __name__ == "__main__":
    sys.exit(main())
