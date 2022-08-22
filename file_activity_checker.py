import ctypes
import datetime
import os
import time
import winsound  # Used in raise_alertN functions, any other action may be written there.


# Parameters
ALERT1_TIMEOUT_MINUTES = 15 + 5     # Main part + extra time
ALERT2_TIMEOUT_MINUTES = 30 + 10    # Main part + extra time
ALERT3_TIMEOUT_MINUTES = 60 + 10    # Main part + extra time
LOCK_TIMEOUT_SECONDS = 10
IS_DBG = False
SLEEP_SECONDS_AFTER_ITERATION = 60  # How much time to sleep before starting next check iteration
SNOOZE_FILE_NAME = 'snooze.txt'
SNOOZE_DATETIME_FORMAT = '%Y-%m-%dT%H%M'  # OLD: '%Y-%m-%dT%H%M%S%'
# TARGET_FILE_NAME = r'D:\Home\Andy\Excel\_2020\2020-01_TimeFormV23.xlsm'
TARGET_FILE_NAME = r'D:\Home\Andy\Excel\_2022\2022-01_TimeFormV25.xlsm'

assert ALERT1_TIMEOUT_MINUTES < ALERT2_TIMEOUT_MINUTES < ALERT3_TIMEOUT_MINUTES


def raise_alert1():
    duration_ms = 100
    freq_hz = 880
    winsound.Beep(freq_hz, duration_ms)


def raise_alert2():
    duration_ms = 200
    freq_hz = 880
    winsound.Beep(freq_hz, duration_ms)
    # time.sleep(0.1)  # There is a natural pause between the beeps (?)
    winsound.Beep(freq_hz, duration_ms * 4)


def raise_alert3():
    duration_ms = 600
    freq_hz = 880
    winsound.Beep(freq_hz, duration_ms)
    # time.sleep(0.1)  # There is a natural pause between the beeps (?)
    winsound.Beep(freq_hz, duration_ms)
    # time.sleep(0.1)  # There is a natural pause between the beeps (?)
    winsound.Beep(freq_hz, duration_ms)


def lock_ws():
    # Lock WS
    ctypes.windll.user32.LockWorkStation()        


def get_snooze_dt():
    snooze_dt = None
    print('  check_if_snoozed: start') if IS_DBG else None

    # Try to open snooze file, if any
    if os.path.isfile(SNOOZE_FILE_NAME):
        print('    snooze file found.') if IS_DBG else None
        with open(SNOOZE_FILE_NAME) as f:
            lines = f.readlines()

        assert len(lines) > 0, 'No lines in the snooze file'
        for i, s in enumerate(lines):
            s = s.strip()
            if i == 0:
                try:
                    snooze_dt = datetime.datetime.strptime(s, SNOOZE_DATETIME_FORMAT)
                    print(f'    parsed snooze dt: {snooze_dt}') if IS_DBG else None
                except:
                    print(f"WARNING! Incorrect snooze file format, expected {SNOOZE_DATETIME_FORMAT}, actual " +
                          f"string '{s}' -> snoozing will be skipped")
                    break
            else:
                assert s == '', f"Unexpected non-empty second or later line: '{s}' in file {SNOOZE_FILE_NAME}"

    else:
        print(f'    file {SNOOZE_FILE_NAME} not found -> snoozing will be skipped') if IS_DBG else None

    return snooze_dt


def get_modification_elapsed_minutes():
    assert os.path.isfile(TARGET_FILE_NAME), f'Cannot find target file {TARGET_FILE_NAME}'
    last_modification_time = os.path.getmtime(TARGET_FILE_NAME)  # Returns unix time in float seconds
    diff_minutes = (time.time() - last_modification_time) / 60.0
    return diff_minutes


def check_target_file_activity():
    # Do the check
    diff_minutes = get_modification_elapsed_minutes()
    if diff_minutes > ALERT3_TIMEOUT_MINUTES:
        print(f'  ..diff {diff_minutes:.1f} m exceeds alert3 timeout {ALERT3_TIMEOUT_MINUTES} m -> ' +
              f'raise alert3 (final). Computer will be locked in {LOCK_TIMEOUT_SECONDS} s')
        raise_alert3()
        # Give last chance to update the target file
        time.sleep(LOCK_TIMEOUT_SECONDS)
        diff_minutes = get_modification_elapsed_minutes()
        if diff_minutes > ALERT3_TIMEOUT_MINUTES:
            lock_ws()

    elif diff_minutes > ALERT2_TIMEOUT_MINUTES:
        print(f'  ..diff {diff_minutes:.1f} m exceeds alert2 timeout {ALERT2_TIMEOUT_MINUTES} m -> ' +
              f'raise alert2. Next alert level timeout: {ALERT3_TIMEOUT_MINUTES}')
        raise_alert2()

    elif diff_minutes > ALERT1_TIMEOUT_MINUTES:
        print(f'  ..diff {diff_minutes:.1f} m exceeds alert1 timeout {ALERT1_TIMEOUT_MINUTES} m -> ' +
              f'raise alert1. Next alert level timeout: {ALERT2_TIMEOUT_MINUTES}')
        raise_alert1()
    else:
        print(f'  ..diff mins {diff_minutes:.1f} does not exceed alert1 timeout minutes {ALERT1_TIMEOUT_MINUTES} -> OK')


def main():
    print('Launching checker (eternal cycle)')
    while True:
        print(f'Check iteration start, dt: {datetime.datetime.now()}')

        snooze_dt = get_snooze_dt()
        if (snooze_dt is not None) and (snooze_dt > datetime.datetime.now()):
            print(f'  .. check snoozed until {snooze_dt}')
        else:
            check_target_file_activity()

        time.sleep(SLEEP_SECONDS_AFTER_ITERATION)


if __name__ == '__main__':
    main()
