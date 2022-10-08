#!/usr/bin/env sh

echo "Removing files..."
rm /etc/rockpro-fan.conf
rm /usr/bin/fancontroller
rm /etc/systemd/system/fancontrol.service

echo "Disabling systemd..."
systemctl disable --now fancontrol
