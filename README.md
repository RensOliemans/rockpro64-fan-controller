# Control fan on RockPro64 according to CPU temperature

This is a simple python script that I use to control fan on RockPro64
SBC running Armbian + OpenMediaVault. All it does is reading
temperature from armbianmonitor, converting it to PWM duty on
dedicated FAN connector and writing it to hwmon, enabling or disabling
the fan.

## Parameters to configure
See `rockpro-fan.conf`.

| Config               | Explanation                                                              |
|----------------------|--------------------------------------------------------------------------|
| TemperatureFile      | File to retrieve temperature from, in millidegrees Celsius               |
| LowSpeedTemperature  | Temperature at which to start blowing the fan slowly                     |
| HighSpeedTemperature | Temperature at which to start blowing the fan at high speed              |
| FanPWMLow            | Speed of slowly blowing fan. Test this out on your machine!              |
| FanPWMHigh           | Speed of quickly blowing fan. 255 is maximum.                            |
| SleepSeconds         | How long to sleep between measurements                                   |
| LoggingLevel         | LoggingLevel (see https://docs.python.org/3/library/logging.html#levels) |


## Run on startup
Install using `make install`. The configfile will be symlinked to
`/etc/rockpro-fan.conf`. It needs to be run with read-access to
`/etc/`, `/usr/bin/` and `/etc/systemd/system/`, running as `root`
will make this work.

## Dealing with changing hwmon name

Actual name of hwmon differs between reboots. Sometimes it is called
hwmon2, the other time hwmon3. In this system there is only one hwmon
anyway, so number is found by polling each name in certain range. This
is not elegant solution and will break if more hwmons are found in a
system.

