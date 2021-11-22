try:
    from threading import Thread
    import logging
    import time
    import random

except Exception as e:
    pass

SLEEP_TIME = 0
MAX_RANGE = 7
MAX_INT = 100

DEBUG_MODE = False

global queue


class Queue(object):
    def __init__(self):
        self.item = []

    def __str__(self):
        return "{}".format(self.item)

    def __repr__(self):
        return "{}".format(self.item)

    def enque(self, item):
        self.item.insert(0, item)
        return True

    def size(self):
        return len(self.item)

    def dequeue(self):
        if self.size() == 0: return None
        else: return self.item.pop()

    def peek(self):
        if self.size() == 0:
            return None
        else:
            return self.item[-1]


class Work(Thread):
    def __init__(self, tab):
        self._Threads = []
        self.queue = Queue()
        self.tab = tab
        self.min = 0
        self.vowel = 0

        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format,
                            level=logging.INFO,
                            datefmt="%H:%M:%S")

    def __str__(self):
        return "Sum: {}; Min: {}; Vowel: {}".format(self.tab[0], self.min, self.vowel)

    def __repr__(self):
        return "Sum: {}; Min: {}; Vowel: {}".format(self.tab[0], self.min, self.vowel)

    def size(self):
        return len(self.tab)

    def sum(self, a, b):
        if DEBUG_MODE:
            logging.info("Thread %s: starting", f"{a} + {b} = ?")
        time.sleep(SLEEP_TIME)
        self.queue.enque(a + b)
        if DEBUG_MODE:
            logging.info("Thread %s: finishing", f"{a} + {b} = ?")

    def min(self, a, b):
        if DEBUG_MODE:
            logging.info("Thread %s: starting", f"{a} < {b} ?")
        time.sleep(SLEEP_TIME)
        self.queue.enque(a > b)
        if DEBUG_MODE:
            logging.info("Thread %s: finishing", f"{a} < {b} ?")

    def sum_it(self, tab):
        tab, ttab = tab, []
        pause = False
        result = []

        while len(tab) != 1:
            if not pause:
                for i in range(0, len(tab), 2):
                    if DEBUG_MODE:
                        logging.info("Create and start thread %d.",
                                     len(self._Threads))
                    _t = Thread(target=self.sum, args=(
                        tab[i],
                        tab[i + 1],
                    ))
                    _t.start()
                    self._Threads.append(_t)

                pause = True
                result = self.result()

                if result[0]:
                    pause = False

                tab, ttab, self._Threads = result[1], [], []

            self.tab = tab
    def sum_it2(self):
        pause = False
        n = 1
        while len(self.tab) != 1:
            n = 0
            if not pause:
                for i in range(0, len(self.tab), 2):
                    n += 2
                    if DEBUG_MODE:
                        logging.info("Create and start thread %d.",
                                     len(self._Threads))
                    _t = Thread(target=self.sum, args=(
                        self.tab[i],
                        self.tab[i + 1],
                    ))
                    _t.start()
                    self._Threads.append(_t)

                pause = True
                result = self.result()

                if result[0]:
                    pause = False

                    self._Threads = []
                    self.tab += result[1]
                    
                    for i in range(0, n):
                      self.tab.pop(0)

    def find_min(self, tab):
        tab = tab
        n = len(tab)
        result = []
        pause = False
        while n != 0:
            for i in range(0, len(tab) - 1):
                if not pause:
                    _t = Thread(target=self.min, args=(
                        tab[i],
                        tab[i + 1],
                    ))

                    _t.start()
                    self._Threads.append(_t)

                    pause = True
                    result = self.result()
                    if result[0]:
                        pause = False
                        if result[1][0]:
                            tab[i], tab[i + 1] = tab[i + 1], tab[i]

            n -= 1
        self.min = tab[0]
        self._Threads = []

    def test_vowel(self, letter):
        self.queue.enque(letter in ["a","e","i","o","u","y"])

    def sum_vowel(self):
        self.Threads = []
        title = "wyliczenia samoglosek"
        result, res = [], []
        pause = False
        for index, l in enumerate(title):
            if not pause:
                _t = Thread(target=self.test_vowel, args=(l))

                _t.start()
                self._Threads.append(_t)

                pause = True
                result = self.result()
                if result[0]:
                    pause = False
                    if result[1][0]:
                      res.append(result[1][0])                        
        self.vowel = sum(res)

    def run(self):
        # self.find_min(self.tab)
        # self.sum_it(self.tab)
        # self.sum_vowel()
        self.sum_it2()

    def result(self):
        result = []
        for index, thread in enumerate(self._Threads):
            if DEBUG_MODE:
                logging.info("before joining thread %d.", index)
            thread.join()
            result.append(self.queue.dequeue())
            if DEBUG_MODE:
                logging.info("thread %d done", index)
        return [True, result]


if __name__ == "__main__":
    # [1, 2, 3, 12, 34, 45, 23, 12, 6, 3, 23, 45, 6, 87, 21, 16]
    t = Work([
        random.randint(0, MAX_INT)
        for i in range([2**i for i in range(MAX_RANGE)][random.randint(
            4, MAX_RANGE - 1)])
    ])
    t.run()
    print(t)
