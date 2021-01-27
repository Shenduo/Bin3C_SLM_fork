#!/usr/bin/env python
from mzd.cluster import *
from mzd.io_utils import load_object, save_object
from mzd.utils import *
import logging
import sys
import os
import argparse

if __name__ == '__main__':


	parser = argparse.ArgumentParser(description="say something about this application !!")
	parser.add_argument("-i", "--input", type=str, help="input contact map")
	parser.add_argument("-o", "--output", type=str, help="output edges")
	result = parser.parse_args()
	 
	print result.input
	print result.output
	
	logging.captureWarnings(True)
	logger = logging.getLogger('main')

	# root log listens to everything
	root = logging.getLogger('')
	root.setLevel(logging.DEBUG)

	# log message format
	formatter = logging.Formatter(fmt='%(levelname)-7s | %(asctime)s | %(name)s | %(message)s')

	# Runtime console listens to INFO by default
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	ch.setFormatter(formatter)
	root.addHandler(ch)

	# File log listens to all levels from root
	log_path = os.path.join(result.output, 'map2g.log')
	if not os.path.exists(result.output):
		os.mkdir(result.output)
	fh = logging.FileHandler(log_path, mode='a')
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)
	root.addHandler(fh)

	# Add some environmental details
	logger.debug(sys.version.replace('\n', ' '))
	logger.debug('Command line: {}'.format(' '.join(sys.argv)))


	cm = load_object(result.input)
	getGraph(cm, result.output)
