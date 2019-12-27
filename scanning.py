import time


def scann_p():
    s = time.time()
    while (time.time() - s) < 60:
        print("Scanning.\r", end="")
        time.sleep(1)
        print("Scanning..\r", end="")
        time.sleep(1)
        print("Scanning...\r", end="")

scann_p()
