import time

from pynput import keyboard
from pynput.keyboard import Key, KeyCode

class TypingTest():
    lastKeyTime = 0
    elapsedTime = 0
    keyPresses = 0
    backspaces = 0
    words = 0
    active = False

    def __init__(self, timeout=10) -> None:
        self.timeout = timeout

    @staticmethod
    def get_char(key):
        if type(key) == KeyCode:
            return key.char
        elif type(key) == Key:
            return key.value.vk
        else:
            return str(key)

    @staticmethod
    def timeSince(t1):
        return abs(time.time() - t1)

    def on_press(self, key):
        #print(self.get_char(key))
        self.keyPresses += 1
        if self.get_char(key) in [49, 36]:
            self.words += 1
        if self.get_char(key) == 51:
            self.backspaces += 1
        if self.lastKeyTime != 0 and self.active:
            self.elapsedTime += self.timeSince(self.lastKeyTime)
        self.lastKeyTime = time.time()
        self.active = True

    def start(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
        )
        listener.start()
        while True:
            if self.timeSince(self.lastKeyTime) >= self.timeout:
                self.active = False


if __name__ == '__main__':
    test = TypingTest()
    try:
        test.start()
    except KeyboardInterrupt:
        print(str(test.words) + ' words')
        print(str(round(test.elapsedTime, 2)) + ' secs')
        print(str(round((test.words/test.elapsedTime)*60, 2)) + ' words/min')
        print(str(round((test.backspaces/test.keyPresses)*100, 2)) + '% error rate')
