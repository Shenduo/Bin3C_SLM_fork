#!/usr/bin/env python
from mzd.cluster import *
from mzd.contact_map import *
from mzd.io_utils import load_object, save_object
from mzd.utils import *

import argparse
import os
import logging
import sys

if __name__ == '__main__':

	def ifelse(arg, default):
		if arg is None:
			return default
		else:
			return arg


	runtime_defaults = {
        'min_reflen': 1000,
        'min_signal': 5,
        'max_image': 4000,
        'min_extent': 50000,
        'min_mapq': 60,
        'strong': 10
    }

	parser = argparse.ArgumentParser()
	parser.add_argument("CL", help="SLM clustering result")
	parser.add_argument("MAP", help="Contact map")
	parser.add_argument('OUTDIR', help='Output directory')
	parser.add_argument('--min-extent', type=int, help='Minimum cluster extent used in output [50000]')
	parser.add_argument('--min-reflen', type=int, help='Minimum acceptable reference length [1000]')
	parser.add_argument('--min-signal', type=int, help='Minimum acceptable signal [5]')
	args = parser.parse_args()

	logging.captureWarnings(True)
	logger = logging.getLogger('main')

    # root log listens to everything
	root = logging.getLogger('')
	root.setLevel(logging.DEBUG)

    # log message format
	formatter = logging.Formatter(fmt='%(levelname)-8s | %(asctime)s | %(name)7s | %(message)s')

    # Runtime console listens to INFO by default
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	ch.setFormatter(formatter)
	root.addHandler(ch)

    # File log listens to all levels from root
	log_path = os.path.join(args.OUTDIR, 'slm2seq.log')
	if not os.path.exists(args.OUTDIR):
		os.mkdir(args.OUTDIR)
	fh = logging.FileHandler(log_path, mode='a')
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)
	root.addHandler(fh)

    # Add some environmental details
	logger.debug(sys.version.replace('\n', ' '))
	logger.debug('Command line: {}'.format(' '.join(sys.argv)))

	logger.info('Loading existing contact map from: {}'.format(args.MAP))
	cm = load_object(args.MAP)
	cm.min_extent = ifelse(args.min_extent, runtime_defaults['min_extent'])

	
	min_reflen = ifelse(args.min_reflen, runtime_defaults['min_reflen'])
	min_signal = ifelse(args.min_signal, runtime_defaults['min_signal'])
	cm.min_len = min_reflen
	cm.min_sig = min_signal
	cm.set_primary_acceptance_mask(min_sig=min_signal, min_len=min_reflen, update=True)
	if cm.processed_map is None:
		cm.prepare_seq_map(norm=True, bisto=True)

	clustering = getSLMresult(cm, args.CL)
	cluster_report(cm, clustering)

	write_fasta(cm, args.OUTDIR, clustering, clobber=True, only_large=False)
	write_report(os.path.join(args.OUTDIR, 'cluster_report.csv'), clustering)
