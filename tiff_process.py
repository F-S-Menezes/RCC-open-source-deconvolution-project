from pathlib import Path
import numpy as np
from skimage.io import imsave,imread
import os, sys, argparse, json, glob

from pycudadecon.affine import deskewGPU
from pycudadecon import decon, rl_cleanup, rl_decon, rl_init, make_otf
#from pycudadecon.util import imread

def json_parser(args):
	"""parses a json file as text and runs a custom operation according to it
	"""
	raw = open(args.json, 'r')
	parms= json.load(raw)
	args.dxdata = parms['pixelWidth']
	args.dzdata = parms['pixelDepth']
	args.angle = parms['angle']
#	args.otf_xy =   ######
	args.otf_z = parms['psfZ']
	args.background = parms['background']
	args.deskew = False if parms['keepDeskew']=="false" else True
	args.destination = parms['outputPath']
	args.psf = parms['psfFile']
	args.folder = parms['path'] ######
	main(args)
	
def process_tiff(tiff, args):
	"""###########################################
	"""
	##rip options from pycudadecon.deskewGPU

	im = imread(tiff)
	deskewed = deskewGPU(im, dxdata=args.options['dxdata'], dzdata=args.options['dzdata'], angle=args.options['angle'])
	
	dirname, fname = os.path.split(tiff)
	fname, ext = os.path.splitext(fname)
	
	if not args.deskew:
		rl_init(deskewed.shape, "otf.tif",dzdata=args.options['dzdata'], dxdata=args.options['dxdata'], dzpsf=args.options['otf_z'], dxpsf=args.options['otf_xy'])
		deconvolved = rl_decon(deskewed, background=args.options['background'])
		imsave(f"{args.destination}/{fname}_deconvolved.tiff", deconvolved, imagej=True)
		rl_cleanup()
	else:
		imsave(f"{args.destination}/{fname}_deskewed.tiff", deskewed, imagej=True)
	
def process_folder(args):
	"""############################################
	"""
	for tiff in glob.glob(args.folder) and not in glob.glob('*otf.tif?'):
		print(tiff)
#		process_tiff(tiff,args)
	
def main(args):
	"""#####################################################
	
	"""
	if args.psf is not None:
		make_otf(args.psf, "otf.tif")
		
	if args.destination is not None and args.files is not None:
		os.makedirs(f"{args.destination}/pycudadecon_output", exist_ok=True)
		args.destination = f"{args.destination}/pycudadecon_output"
	else:
		os.makedirs("pycudadecon_output", exist_ok=True)
		args.destination = "/pycudadecon_output"
		
		
	if args.files is not None:
		for tiff in args.files:
			process_tiff(tiff, args)
		
	if args.folder is not None:
		process_folder(args)
	
if __name__ == "__main__":
	import sys
	
	parser = argparse.ArgumentParser(description='deskew or deconvolve files, or produce an otf file based on given options')
	parser.add_argument('-t', '--files', nargs='+')
	parser.add_argument('-f', '--folder', help='path_to_folder/pattern, needs to be a string')
	parser.add_argument('-p', '--psf')
	parser.add_argument('-j', '--json')
	parser.add_argument('--deskew', action='store_true', help='if set, deskews the data only')
	parser.add_argument('-d', '--destination', help='where to store the file that will contain the processed images')
	parser.add_argument('--dxdata', default = 0.1)
	parser.add_argument('--dzdata', default = 0.5)
	parser.add_argument('--angle', default = 31.5)
	parser.add_argument('--otf_xy', default = 0.1)
	parser.add_argument('--otf_z', default = 0.1)
	parser.add_argument('--background', default ='auto')
	
	##check for json in argparser
	args = parser.parse_args()
	if args.json is not None:
		json_parser(args)
	else:
		main(args)

