#!/bin/bash

WALLDIR="$HOME/Pictures/Wallpapers"

while true; do
    img=$(find "$WALLDIR" -type f | shuf -n 1)
    swww img "$img" --transition-type fade --transition-duration 1
    sleep 60
done
