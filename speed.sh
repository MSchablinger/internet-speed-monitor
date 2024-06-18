#!/bin/bash

# Function to extract the download speed from speedtest-cli output
get_download_speed() {
    speedtest-cli --secure --no-upload | grep -oP 'Download: \K[\d.]+'
}

# Log file for gnuplot data
log_file="speed.log"

# Initialize log file with headers (only if it doesn't exist)
if [ ! -f "$log_file" ]; then
    echo "Date Time DownloadSpeed" > "$log_file"
fi

while true; do
    current_date=$(date '+%Y-%m-%d %H:%M:%S')
    download_speed=$(get_download_speed)
    echo "$current_date $download_speed" >> "$log_file"

    # Convert download speed to an integer
    download_speed_int=$(printf "%.0f" "$download_speed")

    # Determine sleep duration based on download speed
    if (( download_speed_int > 40 )); then
        sleep_duration=10m
    elif (( download_speed_int < 15 )); then
        sleep_duration=0m
    else
        sleep_duration=5m
    fi

    sleep $sleep_duration
done
