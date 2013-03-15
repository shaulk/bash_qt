#!/usr/bin/env python

import sys
import os
import time
import signal
import functools
import shlex
import PyQt4
import PyQt4.QtCore
import PyQt4.QtGui

objects = {}
next_obj = 0
host_pid = 0

def reg_obj(obj):
	global objects, next_obj

	obj_id = next_obj
	next_obj += 1
	objects[obj_id] = obj

	return "obj:" + str(obj_id)

def get_obj(obj_id):
	obj_id = int(obj_id)
	if obj_id in objects:
		return objects[obj_id]
	else:
		return None

def signal_handler(action, *args):
	sys.stdout.write("sig:" + action + " ".join([wrap(x) for x in args]) + "\n")
	sys.stdout.flush()
	while True:
		if call_handler(sys.stdin.readline()) == False:
			break

def signal_registrar(obj, sig_name, action):
	obj.connect(obj, PyQt4.QtCore.SIGNAL(sig_name), functools.partial(signal_handler, action))

def exec_handler(app):
	sys.stdout.write("null\n")
	sys.stdout.flush()
	app.exec_()
	os.kill(host_pid, signal.SIGINT)

def parse_obj_name(obj_name):
	def follow_object_path(start, names):
		obj = start
		for name in names:
			obj = getattr(obj, name)
		return obj
		
	if obj_name.startswith("obj:"):
		names = obj_name.split(".")
		obj = get_obj(names[0][4:])
		return follow_object_path(obj, names[1:])
	elif obj_name.startswith("Qt"):
		names = obj_name.split(".")
		obj = getattr(PyQt4, names[0])
		return follow_object_path(obj, names[1:])
	elif obj_name == "signal":
		return signal_registrar
	elif obj_name == "null":
		return None
	elif obj_name == "exec":
		return exec_handler
	elif obj_name.startswith("[") and obj_name.endswith("]"):
		contents = obj_name[1:-1]
		if contents == "":
			return []
		contents = contents.split(",")
		contents = [parse_obj_name(x) for x in contents]
		return contents
	else:
		# crude handler for numbers
		try:
			num = float(obj_name)
			if "." in obj_name:
				return num
			else:
				return long(num)
		except ValueError:
			return str(obj_name)

def wrap(obj):
	if obj is None:
		return "null"
	elif isinstance(obj, (basestring, int, long, float, PyQt4.QtCore.QString)):
		return str(obj)
	else:
		return reg_obj(obj)

def call_handler(call):
	global sig_queue, waiting_for_sig
	args = shlex.split(call)
	if len(args) == 0:
		return

	if args[0] == "sig_end":
		sys.stdout.write("null\n")
		sys.stdout.flush()
		return False

	args = [parse_obj_name(x) for x in args]
	sys.stdout.write(wrap(args[0](*args[1:])) + "\n")
	sys.stdout.flush()
	return True

def main(args):
	global host_pid
	host_pid = int(args[1])

	while True:
		call_handler(sys.stdin.readline())

if __name__ == "__main__":
	sys.exit(main(sys.argv))

