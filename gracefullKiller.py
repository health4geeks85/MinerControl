import signal
import time
import requests
import atexit


class GracefulKiller:
    killNow = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        signal.signal(signal.SIGHUP, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.killNow = True


if __name__ == "__main__":
    killer = GracefulKiller()
    def setKiller():
        killer.killNow = True

    atexit.register(setKiller)

    while True:
        time.sleep(1)
        print("do something in a loop")
        if killer.killNow:
            requests.get("http://127.0.0.1:8000/kill")
            print("I was killed")
            time.sleep(1)
            break

    print("End of the program")
