import gi
from phue import Bridge, Group, Light

gi.require_version("Plantd", "1.0")

from gi.repository import Plantd  # noqa: E402


class House:
    def __init__(self, ip: str):
        self.bridge = Bridge(ip)
        self.bridge.connect()

    @staticmethod
    def _clamp(min: float, max: float, value: float) -> float:
        return min if value < min else max if value > max else value

    @staticmethod
    def _scale(x_min: float, x_max: float, y_min: float, y_max: float, value: float) -> float:
        return ((y_max - y_min) / (x_max - x_min)) * (value - x_min) + y_min

    def set_room_brightness(self, room: str, brightness: float) -> None:
        try:
            group = Group(self.bridge, room)
            group.brightness = int(brightness)
        except LookupError as e:
            Plantd.error(e)

    def set_room_percentage(self, room: str, percent: float) -> None:
        percent = self._clamp(0, 100, percent)
        brightness = self._scale(0, 100, 0, 254, percent)
        self.set_room_brightness(room, brightness)
