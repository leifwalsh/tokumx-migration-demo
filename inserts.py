#!/usr/bin/env python

import bson
from bson import son
import collections
import itertools
import pymongo
import random
import os
import queue
import sys
import threading
import time

class ChunkGenerator(threading.Thread):
    def __init__(self, iterable, chunksize, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.iterable = iterable
        self.chunksize = chunksize
        self.queue = queue

    @staticmethod
    def chunks(iterator, n):
        '''Given an iterable, yields chunks of size n, where a chunk itself is iterable.'''
        iterator = iter(iterator)
        for first in iterator:
            chunk = itertools.chain((first,), itertools.islice(iterator, n-1))
            yield chunk
            collections.deque(chunk, 0)

    def run(self):
        try:
            for chunk in self.chunks(self.iterable, self.chunksize):
                # Force the computation on this thread
                self.queue.put(list(chunk))
        except KeyboardInterrupt:
            return

def chunks(iterable, chunksize):
    '''Given a (lazy) iterable, and a chunk size, generates and yields chunks of that size and forces the computation on a background thread.'''

    q = queue.Queue(maxsize=3)
    t = ChunkGenerator(iterable, chunksize, q)
    t.start()
    while t.is_alive() or not q.empty():
        try:
            chunk = q.get(True, 1)
            yield chunk
        except queue.Empty:
            pass
    t.join()

assert len(sys.argv) == 4
hosts = sys.argv[1]
ns = sys.argv[2].split('.', 1)
fast = sys.argv[3] == 'fast'

c = pymongo.MongoReplicaSetClient(hosts)
db = c[ns[0]]
col = db[ns[1]]

col.create_index('key1')
col.create_index('key2')
col.create_index('key3')

def generate():
    randints = itertools.starmap(random.randint, itertools.repeat((0, 1000000000)))
    fiftyzeroes = b'0' * 50
    while True:
        s = son.SON(dict(zip(['key1', 'key2', 'key3'], randints)))
        s['val'] = bson.Binary(fiftyzeroes + os.urandom(50))
        yield s

n = 0
try:
    t0 = time.time()
    t = t0
    batchsize = 100
    if fast:
        batchsize = 1000
    for chunk in chunks(generate(), batchsize):
        col.insert(chunk)
        if not fast:
            time.sleep(0.1)

        n += batchsize
        if n % 10000 == 0:
            t2 = time.time()
            print('%07d\t%5.3f/sec\t%5.3f/sec' % (n, (10000 / (t2 - t)), (n / (t2 - t0))))
            t = t2

except KeyboardInterrupt:
    pass
except:
    raise
