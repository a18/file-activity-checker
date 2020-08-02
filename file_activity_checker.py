import datetime
import os
import time
import winsound  # Used in raise_alertN functions, any other action may be written there.


ALERT1_TIMEOUT_SECONDS = (15 + 5) * 60      # 15 minutes + 5 extra minutes
ALERT2_TIMEOUT_SECONDS = (30 + 10) * 60     # 30 minutes + 10 extra minutes
ALERT3_TIMEOUT_SECONDS = (60 + 10) * 60     # 60 minutes + 10 extra minutes
IS_DBG = True
SLEEP_SECONDS = 60  # How much time to sleep after each cycle
SNOOZE_FILE_NAME = 'snooze.txt'
SNOOZE_DATETIME_FORMAT = '%Y-%m-%dT%H%M%S%'
TARGET_FILE_NAME = r'D:\Home\Andy\Excel\_2020\2020-01_TimeFormV23.xlsm'


def raise_alert1():
    duration_ms = 100
    freq_hz = 880
    winsound.Beep(freq_hz, duration_ms)


def raise_alert2():
    duration_ms = 100
    freq_hz = 880
    winsound.Beep(freq_hz, duration_ms)
    time.sleep(0.1)
    winsound.Beep(freq_hz, duration_ms * 3)


def raise_alert3():
    duration_ms = 100
    freq_hz = 880
    winsound.Beep(freq_hz, duration_ms * 3)
    time.sleep(0.1)
    winsound.Beep(freq_hz, duration_ms * 3)
    time.sleep(0.1)
    winsound.Beep(freq_hz, duration_ms * 3)


def get_snooze_dt():
    snooze_dt = None
    print('check_if_snoozed: start') if IS_DBG else None

    # Try to open snooze file, if any
    if os.path.isfile(SNOOZE_FILE_NAME):
        print('  snooze file found.') if IS_DBG else None
        with open(SNOOZE_FILE_NAME) as f:
            lines = f.readlines()

        assert len(lines) > 0, 'No lines in the snooze file'
        for i, s in enumerate(lines):
            s = s.strip()
            if i == 0:
                try:
                    snooze_dt = datetime.datetime.strptime(s, SNOOZE_DATETIME_FORMAT)
                    print(f'  parsed snooze dt: {snooze_dt}') if IS_DBG else None
                except:
                    print(f"WARNING! Incorrect snooze file format, expected {SNOOZE_DATETIME_FORMAT}, actual " +
                          f"string '{s}' -> snoozing will be skipped")
                    break
            else:
                assert s == '', f"Unexpected non-empty second or later line: '{s}' in file {SNOOZE_FILE_NAME}"

    else:
        print(f'  file {SNOOZE_FILE_NAME} not found -> snoozing will be skipped') if IS_DBG else None

    return snooze_dt


def check_target_file_activity():
    # Do the check
    assert os.path.isfile(TARGET_FILE_NAME), f'Cannot find target file {TARGET_FILE_NAME}'
    last_modification_time = os.path.getmtime(TARGET_FILE_NAME)
    diff_seconds = time.time() - last_modification_time
    if diff_seconds > ALERT3_TIMEOUT_SECONDS:
        print(f'..diff secs {diff_seconds:.1f} exceeds alert3 timeout seconds {ALERT3_TIMEOUT_SECONDS} -> raise alert3')
        raise_alert3()
    elif diff_seconds > ALERT2_TIMEOUT_SECONDS:
        print(f'..diff_secs {diff_seconds:.1f} exceeds alert2 timeout seconds {ALERT2_TIMEOUT_SECONDS} -> raise alert2')
        raise_alert2()
    elif diff_seconds > ALERT1_TIMEOUT_SECONDS:
        print(f'..diff_secs {diff_seconds:.1f} exceeds alert1 timeout seconds {ALERT1_TIMEOUT_SECONDS} -> raise alert1')
        raise_alert1()
    else:
        print(f'..diff_secs {diff_seconds:.1f} does not exceed alert1 timeout seconds {ALERT1_TIMEOUT_SECONDS} -> OK')


def main():
    print('Launching checker')
    while True:
        print(f'Cycle start, dt: {datetime.datetime.now()}')

        snooze_dt = get_snooze_dt()
        if (snooze_dt is not None) and (snooze_dt > datetime.datetime.now()):
            print(f'.. check snoozed until {snooze_dt}')
        else:
            check_target_file_activity()

        time.sleep(SLEEP_SECONDS)


if __name__ == '__main__':
    main()
