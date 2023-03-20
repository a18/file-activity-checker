import winsound
import time

# SLEEP_IN_SECONDS = 5 * 60.0  # 5 mins
SLEEP_IN_SECONDS = 1.0
FREQ_HZ = 1000
DURATION_MS = 1

while True:
    print("Beep")
    winsound.Beep(frequency=FREQ_HZ, duration=DURATION_MS)
    time.sleep(SLEEP_IN_SECONDS)
