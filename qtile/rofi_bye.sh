#!/bin/bash

chosen=$(printf "  Power Off\n  Restart\n  Suspend\n" | rofi -dmenu -i)

case "$chosen" in
	"  Power Off") systemctl poweroff ;;
	"  Restart") reboot ;;
	"  Suspend") systemctl suspend ;;
	*) exit 1 ;;
esac
