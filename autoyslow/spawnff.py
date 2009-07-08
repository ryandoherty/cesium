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
    if len(page_list) == 0:
        time.sleep(60.0);
        return

    # config stuff TODO: this will be pulled out into a config file
    browser_loc = "/Applications/Firefox.app/Contents/MacOS/firefox"
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
        args = [browser_loc, "-no-remote", "--display=:0"]
        args.extend(page_list[curr_first:(curr_first+loads_per_proc)])
        print "Starting Firefox."
        proc = subprocess.Popen(args)
        print "Sleeping..."
        time.sleep(float(loads_per_proc * page_timeout))
        print "Killing Firefox."
        proc.kill()
        if curr_first + loads_per_proc > len(page_list):
            loads_per_proc = len(page_list) - curr_first
        else:
            curr_first += loads_per_proc

    # quick fix to keep multiple tests from being scheduled
    if len(page_list) * loads_per_proc < 60.0:
        time.sleep(60.0 - (len(page_list) * loads_per_proc))
