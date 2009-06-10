#!/usr/bin/env python

import threading
import subprocess
import time

lock = threading.Lock()

def run_test(browser_loc, page_list):
	# config stuff
	loads_per_proc = 10
	page_timeout = 15	# per web page

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
		print "Pages " + str(curr_first) + "-" + str(curr_first+loads_per_proc) + " of " + str(len(page_list))
		args = ["sudo", browser_loc, "--display=:0"]
		args.extend(page_list[curr_first:(curr_first+loads_per_proc)])
		print args
		test = Test(arg_arr=args, timeout=(loads_per_proc*page_timeout))
		test.start()
		if curr_first + loads_per_proc > len(page_list):
			loads_per_proc = len(page_list) - curr_first
		else:
			curr_first += loads_per_proc

class Test(threading.Thread):
	def __init__(self, arg_arr, timeout):
		self.arg_arr = arg_arr
		self.timeout = timeout
		print(self.timeout)
		print(self.arg_arr)
		threading.Thread.__init__(self)
	
	def run(self):
		lock.acquire()
		print "Spawning Firefox"
		proc = subprocess.Popen(self.arg_arr)
		time.sleep(float(self.timeout))
		proc.kill()
		print "Killed process..."
		lock.release()
