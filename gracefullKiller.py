import signal
import time
import requests
import win32api

class GracefulKiller:
    killNow = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        # windows
        signal.signal(signal.SIGABRT, self.exit_gracefully)
        signal.signal(signal.SIGSEGV, self.exit_gracefully)
        signal.signal(signal.SIGILL, self.exit_gracefully)
        signal.signal(signal.SIGFPE, self.exit_gracefully)

        win32api.SetConsoleCtrlHandler(self.win_exit, True)
        
       # signal.signal(signal.SIGHUP, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.killNow = True

    def win_exit(self, func=None):
        self.killNow = True


if __name__ == "__main__":
    killer = GracefulKiller()
    requests.get("http://127.0.0.1:8000/start")
    

    while True:
        try:
            time.sleep(1)
        except InterruptedError:
            killer.killNow = True
            
        print("do something in a loop")
        if killer.killNow:
            requests.get("http://127.0.0.1:8000/kill")
            print("I was killed")
            time.sleep(1)
            break

    print("End of the program")
