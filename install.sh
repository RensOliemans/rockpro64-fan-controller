#!/usr/bin/env sh

me=$PWD

echo "Installing files..."
ln -s $PWD/rockpro-fan.conf /etc
ln -s $PWD/fancontroller /usr/bin
ln -s $PWD/fancontrol.service /etc/systemd/system

echo "Adding and (auto)starting systemd..."
systemctl daemon-reload
systemctl enable --now fancontrol
