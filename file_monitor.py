
#!/usr/bin/env python

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pynput.keyboard import Controller, Key

class FileCreationHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.keyboard = Controller()

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"New file created: {event.src_path}")
        self.press_enter()

    def press_enter(self):
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        print("Enter pressed")

def monitor_directory(directory):
    event_handler = FileCreationHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_to_monitor = "C:\\Users\\Ben\\Documents\\Warcraft III\\BattleNet\\456125292\\Replays\\Autosaved\\Multiplayer"
    monitor_directory(directory_to_monitor)