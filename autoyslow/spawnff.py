#!/usr/bin/env python

import threading
import subprocess
import time

# Since each site could potentially load hundreds of pages, this code loads 
# ten pages in a single instance of Firefox, kills that instance, then 
# repeats until all the requested pages have been loaded.  Since only one 
# instance of Firefox can be run at any one time, we wait on the current  
# thread to prevent multiple threads from trying to open Firefox at the 
# same time
def run_test(page_list):
    # config stuff TODO: this will be pulled out into a config file
    browser_loc = "/usr/bin/firefox"
    loads_per_proc = 10
    page_timeout = 15    # per web page

    # figure out the exact bounds on how many times we have to iterate
    extra_round = 0
    if len(page_list) % loads_per_proc != 0:
        extra_round = 1
    if len(page_list) < loads_per_proc:
        loads_per_proc = len(page_list)
        extra_round = 0
        # iterate through, loading loads_per_proc number of pages per go around
    curr_first = 0
    for i in range((len(page_list) / loads_per_proc)+extra_round):
        args = ["sudo", browser_loc, "-no-remote", "--display=:0"]
        args.extend(page_list[curr_first:(curr_first+loads_per_proc)])
        proc = subprocess.Popen(self.arg_arr)
        time.sleep(float(loads_per_proc * page_timeout))
        proc.kill()
        #test = Test(arg_arr=args, timeout=(loads_per_proc*page_timeout))
        #test.start()
        #test.join()
        if curr_first + loads_per_proc > len(page_list):
            loads_per_proc = len(page_list) - curr_first
        else:
            curr_first += loads_per_proc

class Test(threading.Thread):
    def __init__(self, arg_arr, timeout):
        self.arg_arr = arg_arr
        self.timeout = timeout
        threading.Thread.__init__(self)
    
    def run(self):
        print "Spawning Firefox"
        proc = subprocess.Popen(self.arg_arr)
        print "sleeping..."
        time.sleep(float(self.timeout))
        proc.kill()
        print "Killed process..."

if __name__ == '__main__':
    import sys
    print "main"
    run_test(sys.argv[1], sys.argv[2:])
