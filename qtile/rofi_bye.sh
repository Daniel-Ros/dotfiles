#!/bin/bash

chosen=$(printf "  Power Off\n  Restart\n  Suspend\nReload Config" | rofi -dmenu -i)

case "$chosen" in
	"  Power Off") systemctl poweroff ;;
	"  Restart") reboot ;;
	"  Suspend") systemctl suspend ;;
	"Reload Config") qtile cmd-obj -o cmd -f reload_config ;;
	*) exit 1 ;;
esac