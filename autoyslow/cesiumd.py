#!/usr/bin/env python

import re
import threading
import socket
import pickle
import datetime
import spawnff
import os
import sys

sys.path.append('..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cesium.settings'
import cesium.settings
from cesium.autoyslow.models import Site

class CesiumDaemon(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.pq = PriorityQueue()
        self.next_test = None
        self.server_thread = self.ServerThread(port, self)
    
    def run(self):    
        self.server_thread.start()
 
    class ServerThread(threading.Thread):
        def __init__(self, port, daemon):
            threading.Thread.__init__(self)
            self.daemon = daemon
            self.ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ssock.bind(('localhost', port))
            self.ssock.listen(5)
 
        def run(self):
            while True:
                (client_socket, address) = self.ssock.accept()
                self.CommThread(self.daemon, client_socket).start()
   
        # thread to deal with incoming requests to the daemon 
        class CommThread(threading.Thread):
            def __init__(self, daemon, sock):
                self.client_sock = sock
                threading.Thread.__init__(self)
                self.daemon = daemon    
    
            def run(self):
                client_msg = ''.join(self.recv_til_done())
                blob = pickle.loads(client_msg)
                self.daemon.pq.push(blob.site_id, blob.new_dt)
                self.daemon.notify_update()
                self.client_sock.close()
    
            def recv_til_done(self):
                # the suggested buffer size by the python docs is 4096
                client_msg = self.client_sock.recv(4096)
                while client_msg:
                    print "Received %d bytes" % len(client_msg)
                    yield client_msg
                    client_msg = self.client_sock.recv(4096)
                print "Server receive complete"
                yield ''
    
            def send_til_done(self, msg):
                total = 0
                while total < len(msg):
                    total += self.client_sock.send(msg[total:])
                self.client_sock.shutdown(socket.SHUT_WR)
                print "Server send complete"
 
    # must be called to notify this thread of an update to the test PQ
    def notify_update(self):
        print "Received PQ update notification."
        print "Current PQ: %s" % self.pq
        next = self.pq.priority_peek()
        if next == (None, None):
            print "Nothing in the PQ..."
            return

        now = datetime.datetime.now()
        seconds_per_day = 86400  # 24*60*60
        tdelta = next[1] - now
        # screw microseconds
        delay = tdelta.days * seconds_per_day + tdelta.seconds
        
        if self.next_test != None:
            self.next_test.cancel()
        self.next_test = threading.Timer(delay, self.runtest_wrapper)
        self.next_test.start()
        print "Started the next test countdown for %d seconds." % delay

    def notify_complete(self, site_id):
        self.next_test = None
        print "Test complete."
        self.pq.push(site_id, Site.objects.get(id=site_id).next_test_time())
        self.notify_update()

    # wrapper to hand to the threading.Timer object -- runs whatever is at 
    # the top of the PQ when it gets executed
    def runtest_wrapper(self):
        site_id = self.pq.pop()
        # this should never happen, but just in case
        if site_id == None:
            print "Error in runtest_wrapper(): site_id should not be None"
            return
        site = Site.objects.get(id=site_id)
        pages = [(site.base_url + page.url) for page in site.page_set.all()]
        spawnff.run_test(pages)
        self.notify_complete(site_id)

class CesiumClient(object):
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', port))

    def update_site(self, site_id, new_dt):
        """Sends the new datetime of the given site's next run to the daemon
            to update it.
        """
        msg = pickle.dumps(DataBlob(site_id, new_dt))
        self.send_til_done(msg)

    def recv(self):
        to_return = ''.join(self.recv_til_done())
        self.sock.close()
        return ''.join(self.recv_til_done())   
 
    def send_til_done(self, msg):
        total = 0
        while total < len(msg):
            total += self.sock.send(msg[total:])
        self.sock.shutdown(socket.SHUT_WR)
        print "Client send complete"

    def recv_til_done(self):
        # the suggested buffer size by the python docs is 4096
        msg = self.sock.recv(4096)
        while msg:
            print "Received %d bytes" % len(msg)
            yield msg
            msg = self.sock.recv(4096)
        print "Client receive complete"
        yield ''

# class to contain data to pickle for transmission
class DataBlob(object):
    def __init__(self, site_id, new_dt):
        self.site_id = site_id
        self.new_dt = new_dt

# TODO: since we're using Python 2.6 now, which does include a PriorityQueue
# class, we might want to look into getting rid of this class in favor of 
# something built into the language 
class PriorityQueue(object):
    """This is a thread-safe priority queue that does not allow duplicate 
    elements, and instead updates the priority of anything that already 
    exists in the queue.
    """
    
    def __init__(self):
        self.heap = []
        self.set = set()
        self.lock = threading.Lock()

    def peek(self):
        item = None
        self.lock.acquire()
        try:
            if len(self.heap) > 0:
                item = self.heap[0][0]
        finally:
            self.lock.release()
        return item

    def priority_peek(self):
        item, priority = None, None
        self.lock.acquire()
        try:
            if len(self.heap) > 0:
                item, priority = self.heap[0]
        finally:
            self.lock.release()
        return item, priority 

    def push(self, item, priority):
        self.lock.acquire()
        
        try:
            #self._check_min_heap_invariant()
            if item in self.set:
                idx = 0
                for i in range(len(self.heap)):
                    if item == self.heap[i][0]:
                        idx = i
                        break
                old_priority = self.heap[idx][1]
                self.heap[idx] = (item, priority)
                if priority > old_priority:
                    self._percolate_down(self.heap[idx], idx)
                else:
                    self._percolate_up(self.heap[idx], idx)
            else:
                self.heap.append((item, priority))
                self._percolate_up(self.heap[-1], len(self.heap)-1)
                self.set.add(item)
            #self._check_min_heap_invariant()
        finally:
            self.lock.release()
    
    def pop(self):
        item = None
        self.lock.acquire()
        try:
            if len(self.heap) > 0:
                #self._check_min_heap_invariant()
                item = self.heap[0][0]
                self.heap[0] = self.heap[-1]
                del self.heap[-1]
                if len(self.heap) > 0:
                    self._percolate_down(self.heap[0])
                self.set.remove(item)
                #self._check_min_heap_invariant()
        finally:
            self.lock.release()
        return item
    
    def _percolate_up(self, elem, root):
        # gets the correct parent index based on the root's parity
        parent = (root - 2 + (root % 2)) / 2
        
        if root == 0 or elem[1] >= self.heap[parent][1]:
            self.heap[root] = elem
            return
        self.heap[root] = self.heap[parent]
        # suck it, guido
        return self._percolate_up(elem, parent)

    def _percolate_down(self, elem, root=0):
        child0, child1 = (root * 2) + 1, (root * 2) + 2     
        if child0 >= len(self.heap):
            self.heap[root] = elem
            return
        elif child1 >= len(self.heap):
            # this is very specific to a PQ with datetime as the priority...
            # suggestions?
            p1 = datetime.datetime.max
        else:
            p1 = self.heap[child1][1]
        p0 = self.heap[child0][1]

        if elem[1] > p0 or elem[1] > p1:
            if p0 < p1:
                self.heap[root] = self.heap[child0]
                return self._percolate_down(elem, child0)
            else:
                self.heap[root] = self.heap[child1]
                return self._percolate_down(elem, child1)
        else:
            self.heap[root] = elem
            return

    def __str__(self):
        return str(self.heap)

    # this method is just for ensuring that the heap obeyed its invariant 
    # during testing
    def _check_min_heap_invariant(self, root=0):
        if len(self.heap) == 0:
            return
        child0, child1 = (root * 2) + 1, (root * 2) + 2
        if child0 > len(self.heap)-1:
            return
        elif child1 > len(self.heap)-1:
            if self.heap[root][1] > self.heap[child0][1]:
                raise ValueError, "Min-heap invariant violated: %d, %s" % (root, self.heap)
            return self._check_min_heap_invariant(child0)
        if self.heap[root][1] > self.heap[child0][1] or\
            self.heap[root][1] > self.heap[child1][1]:
            raise ValueError, "Min-heap invariant violated: %d, %s" % (root, self.heap)
        else:
            self._check_min_heap_invariant(child0)
            return self._check_min_heap_invariant(child1)

if __name__ == '__main__':
    daemon.DaemonContext().open()
    CesiumDaemon(cesium.settings.AUTOYSLOW_DAEMON_PORT).start()
