#!/bin/bash
[[ $EUID -ne 0 ]] && echo "Need root" && exit 1

apt install -y libusb-1.0 libudev-dev

cat >> /etc/udev/rules.d/99-mcp2221.rules << EOL
# /etc/udev/rules.d/99-mcp2221.rules
SUBSYSTEM=="usb", ATTRS{idVendor}=="04d8", ATTR{idProduct}=="00dd", MODE="0666"
EOL

# Disable hid_mcp2221 kernel mod
rmmod hid_mcp2221
echo blacklist hid_mcp2221 > /etc/modprobe.d/blacklist-hid_mcp2221.conf
update-initramfs -u

pip3 install hidapi
pip3 install adafruit-blinka

export BLINKA_MCP2221=1