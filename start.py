import csv
import subprocess
import time
import datetime
import re
import logging
from collections import deque
import threading
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s')
speed_log = 'speed.log'

try:
    with open(speed_log, 'x') as f:
        f.write("Date Time DownloadSpeed\n")
except FileExistsError:
    pass

def get_download_speed():
    try:
        result = subprocess.run(['speedtest-cli',  '--no-upload'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logging.error(f"speedtest-cli command failed: {result.stderr}")
            return None

        match = re.search(r'Download: ([\d.]+) Mbit/s', result.stdout)
        if match:
            return float(match.group(1))
        else:
            logging.warning("Download speed not found in speedtest-cli output")
            return None
    except Exception as e:
        logging.error(f"Error executing speedtest-cli: {e}")
        return None

def log_speed(download_speed):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(speed_log, 'a') as f:
        f.write(f"{current_time} {download_speed}\n")
def speed_test():
    last_5_speeds = deque(maxlen=5)
    while True:
        download_speed = get_download_speed()
        if download_speed is None:
            time.sleep(60)
            continue

        log_speed(download_speed)

        last_5_speeds.append(download_speed)

        if download_speed > 40:
            sleep_duration = 600  # 10 minutes
        elif any(speed < 15 for speed in last_5_speeds):
            sleep_duration = 0  # do not wait
        else:
            sleep_duration = 300  # 5 minutes

        time.sleep(sleep_duration)
if __name__ == '__main__':
    speed_test_thread = threading.Thread(target=speed_test)
    speed_test_thread.daemon = True      
    speed_test_thread.start()
    try:
        subprocess.run(["flask", "run", "--host=0.0.0.0"])
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program.")
