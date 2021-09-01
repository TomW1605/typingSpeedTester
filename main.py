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
            self.wordsStr = str(self.words)
            self.timeStr = str(round(self.elapsedTime, 2))
            self.wordsPerMinStr = str(round((self.words / self.elapsedTime) * 60, 2)) if self.elapsedTime != 0 else 0
            self.errorRateStr = str(round((self.backspaces / self.keyPresses) * 100, 2)) if self.keyPresses != 0 else 0
            print('{:>5}'.format(self.wordsStr) + '\t' +
                  '{:>4}'.format(self.timeStr) + '\t' +
                  '{:>9}'.format(self.wordsPerMinStr) + '\t' +
                  '{:>12}'.format(self.errorRateStr) + '\t' +
                  str(self.active) + ' ',
                  end='\r')


if __name__ == '__main__':
    typingTest = TypingTest(5)
    try:
        print('words\ttime\twords/min\t% error rate\tactive')
        typingTest.start()
    except KeyboardInterrupt:
        wordsStr = str(typingTest.words)
        timeStr = str(round(typingTest.elapsedTime, 2))
        wordsPerMinStr = str(round((typingTest.words / typingTest.elapsedTime) * 60, 2)) if typingTest.elapsedTime != 0 else 0
        errorRateStr = str(round((typingTest.backspaces / typingTest.keyPresses) * 100, 2)) if typingTest.keyPresses != 0 else 0
        print('\n')
        print(wordsStr + ' words')
        print(timeStr + ' secs')
        print(wordsPerMinStr + ' words/min')
        print(errorRateStr + '% error rate')
