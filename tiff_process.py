from pathlib import Path
import numpy as np
from skimage.io import imsave,imread
import os, sys, argparse

from pycudadecon.affine import deskewGPU
from pycudadecon import decon, rl_cleanup, rl_decon, rl_init, make_otf
#from pycudadecon.util import imread

def json_parser(json):
	"""parses a json file as text and runs a custom operation according to it
	"""
	raw = open(json, "r")
	pairs = raw.read().splitext(',')
	for pair in pairs:
		key, value = pair.splitext(':')
	
def process_tiff(tiff, mode):
	"""processes a single tiff file
	"""
	
	if tiff.endswith(('.tiff', '.tif')):
		dirname, fname = os.path.split(tiff)
		fname, ext = os.path.splitext(fname)
		im = imread(tiff)
		deskewed = deskewGPU(im)
		if not mode:
			rl_init(deskewed.shape, f"psf_otf.tif",)
			deconvolved = rl_decon(deskewed, background='auto')
			imsave(f"{fname}_deconvolved.tiff", deconvolved, imagej=True)
			rl_cleanup()
		else:
			imsave(f"{fname}_deskewed.tiff", deskewed, imagej=True)
	else:
		print("encountered file of incompatiple type:", tiff)
		sys.exit(2)
		
	
def process_folder(folder, mode):
	"""prrocesses a folder assumed to only contain tiff files to 
	"""
	for file in folder:
		process_tiff(file, mode)

def main(args):
	"""deskew, deconvolve, and/or produce an otf file based on given options
	
	PARAMETERS:
	
	"""
	if args.psf is not None:
		make_otf(args.psf)
		
	if args.tiff is not None:
		process_tiff(args.tiff, args.deskew)
		
	if args.folder is not None:
		process_folder(args.folder, args.deskew)
	
if __name__ == "__main__":
	import sys
	
	parser = argparse.ArgumentParser(description='deskew, deconvolve, or produce an otf file based on given options')
#	parser.add_argument('-d', '--dest')
	parser.add_argument('-t', '--tiff')
	parser.add_argument('-f', '--folder')
	parser.add_argument('-p', '--psf')
	parser.add_argument('-j', '--json')
	parser.add_argument('-d', '--deskew', action='store_true')
	
	##check for json in argparser
	args = parser.parse_args()
	if args.json is not None:
		json_parser(args.json)
	else:
		main(args)

