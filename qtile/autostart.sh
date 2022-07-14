#!/bin/bash


nitrogen --restore &
xrandr --output HDMI-A-0 --left-of DisplayPort-0 &
setxkbmap -layout "us,il" -option "grp:alt_shift_toggle"&

