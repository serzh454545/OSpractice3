import threading
import queue
import random
import time


def produce(queue, event):
    while not event.is_set():
        if queue.qsize() <= 80:
            item = random.randint(1, 100)
            queue.put(item)
        else:
            while not event.is_set() and queue.qsize() > 80:
                time.sleep(1)


def consume(queue, event):
    while not event.is_set():
        if not queue.empty():
            item = queue.get()
            time.sleep(0)


if __name__ == '__main__':
    queue = queue.Queue()
    for i in range(100):
        queue.put(i)

    reduce_stop = threading.Event()
    produce_stop = threading.Event()
    workers = [
        threading.Thread(target=produce, args=(queue, reduce_stop,)),
        threading.Thread(target=produce, args=(queue, reduce_stop,)),
        threading.Thread(target=produce, args=(queue, reduce_stop,)),
        threading.Thread(target=consume, args=(queue, produce_stop,)),
        threading.Thread(target=consume, args=(queue, produce_stop,))
    ]
    for w in workers:
        w.start()

    while True:
        if input('Press q for stop produce: ') == 'q':
            reduce_stop.set()
            while not queue.empty():
                pass
            produce_stop.set()
            break

    for w in workers:
        w.join()