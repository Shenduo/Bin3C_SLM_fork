#!/usr/bin/env python
from mzd.cluster import *
from mzd.io_utils import load_object, save_object
from mzd.utils import *
import logging
import sys
import os

if __name__ == '__main__':
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
	log_path = os.path.join('/media/sf_dataset/', 'map2g.log')
	fh = logging.FileHandler(log_path, mode='a')
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)
	root.addHandler(fh)

	# Add some environmental details
	logger.debug(sys.version.replace('\n', ' '))
	logger.debug('Command line: {}'.format(' '.join(sys.argv)))

	cm = load_object('/media/sf_dataset/bin3C_scaf_S/contact_map.p.gz')
	getGraph(cm, '/media/sf_dataset/')
