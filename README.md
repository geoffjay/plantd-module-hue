# Plantd Module for Hue Lighting

This is a simple `plantd` device to interact with a Hue lighting system. There
are various requirements to running this and setup and execution is not
documented well enough yet to be useful.

## Changing a Room

An example of changing the brightness for a group of lights named "Spare
Bedroom".

```python
import gi

gi.require_version("Pd", "1.0")

from gi.repository import Pd


client = Pd.Client.new("tcp://<broker ip>:7200")
request = Pd.JobRequest()
request.set_id("hue")
request.set_job_id("change-room")
request.set_job_value("Spare Bedroom")
request.add(Pd.Property.new("brightness", "127"))
client.send_request("hue", "submit-job", request.serialize())
```
