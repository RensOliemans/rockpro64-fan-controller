#!/usr/bin/env python

import time
import os
import configparser

from collections.abc import Iterator

DEFAULT_CONFIGFILE = '/etc/rockpro-fan.conf'

class FanController:
    def __init__(self, configfile=DEFAULT_CONFIGFILE):
        self._configfile = configfile
        self.config = self._load_config()

    def _load_config(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        with open(self._configfile) as stream:
            config.read_string("[top]\n" + stream.read())
        return config['top']

    def run(self) -> None:
        while True:
            temp = self._get_temperature()
            speed = self._determine_speed_percentage(temp)
            self._set_fan_speed(speed)
            print(f"CPU temperature: {temp} °C")
            self._sleep()

    def _get_temperature(self) -> float:
        with open(self.config['TemperatureFile'], 'r') as f:
            return int(f.read()) / 1000

    def _determine_speed_percentage(self, temp: float) -> float:
        low = float(self.config['LowSpeedTemperature'])
        high = float(self.config['HighSpeedTemperature'])

        percentage = (temp - low) / (high - low)
        # Return percentage if it's between 0 and 1
        return min(
            max(0,
                percentage),
            1
        )

    def _set_fan_speed(self, speed_percentage: float) -> None:
        assert speed_percentage >= 0, "Speed percentage should be positive"
        assert speed_percentage <= 1, "Speed percentage cannot exceed 1"

        speed_integer = self._determine_speed_integer(speed_percentage)
        self._set_pwm(speed_integer)

    def _determine_speed_integer(self, speed_percentage: float) -> int:
        low = int(self.config['FanPWMLow'])
        high = int(self.config['FanPWMHigh'])
        assert high >= low, "FAN_PWM_HIGH should be higher than FAN_PWM_LOW"

        difference = high - low
        extra = speed_percentage * difference
        return round(extra + low)

    def _set_pwm(self, speed: int) -> None:
        valid_devices = self._get_existing_device_filenames()
        for device in valid_devices:
            self._set_pwm_of_device(device, speed)

    def _get_existing_device_filenames(self) -> Iterator[str]:
        hardcoded_hwmon_max_amount = 16
        hardcoded_hwmon_path = "/sys/devices/platform/pwm-fan/hwmon/hwmon{id}/pwm1"

        for hwmon_id in range(hardcoded_hwmon_max_amount):
            filename = hardcoded_hwmon_path.format(id=hwmon_id)
            if os.path.exists(filename):
                yield filename

    def _set_pwm_of_device(self, filename: str, speed: int) -> None:
        print(f"Setting {speed} of {filename}")
        with open(filename, "w") as f:
            f.write(str(speed))

    def _sleep(self) -> None:
        time.sleep(int(self.config['SleepSeconds']))


def main():
    fancontroller = FanController()
    fancontroller.run()


if __name__ == '__main__':
    main()
