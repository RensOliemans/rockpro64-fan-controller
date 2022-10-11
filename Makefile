install:
	echo "Installing files..."
	ln -s $PWD/rockpro-fan.conf /etc
	ln -s $PWD/fancontroller /usr/bin
	ln -s $PWD/fancontrol.service /etc/systemd/system

	echo "Adding and (auto)starting systemd"
	systemctl daemon-reload
	systemctl enable --now fancontrol


uninstall:
	echo "Removing files..."
	rm /etc/rockpro-fan.conf
	rm /usr/bin/fancontroller
	rm /etc/systemd/system/fancontrol.service

	echo "Disabling systemd..."
	systemctl disable --now fancontrol
