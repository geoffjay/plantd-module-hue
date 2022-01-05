from phue import Bridge


class House:
    def __init__(self):
        self.bridge = Bridge("10.10.10.101")
        self.bridge.connect()
        self.light_names = self.bridge.get_light_objects("name")

    @staticmethod
    def _clamp(min: float, max: float, value: float) -> float:
        return min if value < min else max if value > max else value

    @staticmethod
    def _scale(x_min: float, x_max: float, y_min: float, y_max: float, value: float) -> float:
        return ((y_max - y_min) / (x_max - x_min)) * (value - x_min) + y_min

    def set_room_brightness(self, room: str, brightness: float) -> None:
        lights = {key: value for (key, value) in self.light_names.items() if key.startswith(room)}
        for light in lights.values():
            light.brightness = brightness

    def set_room_percentage(self, room: str, percent: float) -> None:
        percent = self._clamp(0, 100, percent)
        brightness = self._scale(0, 100, 0, 254, percent)
        return self.set_room_brightness(room, brightness)
