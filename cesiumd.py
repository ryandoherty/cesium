#!/usr/bin/env python

import threading, socket

class CesiumDaemon(object):
    def __init__(self, port):
        test_pq = PriorityQueue()
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.bind(('localhost', port))
        serversock.listen(5)
        while True:
            (client_socket, address) = serversock.accept()
            self.CesiumThread(client_socket).start()
    
    class CesiumThread(threading.Thread):
        def __init__(self, sock):
            self.client_sock = sock
            threading.Thread.__init__(self)
    
        def run(self):
            client_msg = ''.join(self.recv_til_done())
            self.send_til_done(client_msg)

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

class CesiumClient(object):
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', port))

    def recv(self):
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
                item = self.heap[0]
        finally:
            self.lock.release()
        return item

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
            p1 = float('inf')
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
