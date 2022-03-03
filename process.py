from pathlib import Path
from skimage.io import imsave,imread
import os, sys, argparse, json, glob

from pycudadecon import decon, rl_cleanup, rl_decon, rl_init, make_otf, deskewGPU

def json_parser(args):
	"""parses a json file as text and runs a custom operation according to it.
	
	ANY OTHER SET OPTIONS WILL BE IGNORED
	
	REQUIRED OPTIONS TO BE SET:
		--json
	"""
	raw = open(args.json, 'r')
	parms= json.load(raw)
	
###values that get over-written
	
	args.dxdata = max(parms['pixelWidth'], parms['pixelHeight'])
	args.dzdata = parms['pixelDepth']
	args.angle = parms['angle']
	args.otf_xy =  parms['psfDr'] 
	args.otf_z = parms['psfZ']
	args.background = parms['background']

##comment out the above if testing using default values

	args.deskew = parms['deskew']
	args.keep_deskew = parms['keepDeskew']
	args.destination = parms['outputPath']
	args.psf = parms['psfFile']
	if parms['isfolder']:
		args.folder = parms['path']
	else:
		args.files = [parms['path']]
		
	main(args)
	
def process_tiff(tiff, args):
	"""deconvolutes or only deskews a single tiff file, if otf was created by this process, deconvolutes using that otf, or an otf specified by --otf, or otheriwse by a file in $PWD named 'otf.tif'.
	
	--otf will be ignored if --psf was used
	
	PARAMETERS:
	tiff (string): path to a single tif/tiff file
	args (argparse.namespace): argparser structure
	
	REQUIRED OPTIONS TO BE SET:
		at least one of --files or --folder
	"""

	dirname, fname = os.path.split(tiff)
	fname, ext = os.path.splitext(fname) ##store the filename
	
	im = imread(tiff)
	
	if args.deskew==False: ##file is not deskewed, deskew before deconvolution
		deskewed = deskewGPU(im, dxdata=args.dxdata, dzdata=args.dzdata, angle=args.angle)
	else:
		deskewed = im
	
	if args.keep_deskew==True: ##deskewed file is to be saved seperately
		imsave(f"{args.destination}/{fname}_deskewed.tiff", deskewed, imagej=True)
		
	if args.psf is not None:
		otf_source = f"{args.destination}/otf.tif"
	elif args.otf is not None:
		otf_source = args.otf
	else:
		otf_source = "otf.tif"
	
	rl_init(deskewed.shape, f"{otf_source}",dzdata=args.dzdata, dxdata=args.dxdata, dzpsf=args.otf_z, dxpsf=args.otf_xy)
	deconvolved = rl_decon(deskewed, background=args.background)
	rl_cleanup()
	imsave(f"{args.destination}/{fname}_deconvolved.tiff", deconvolved, imagej=True)
	
	
def process_folder(args):
	"""looks in the folder given as part of args.folder for files matching the pattern at the end.
	SKIPS FILES ENDING IN otf
	
	REQUIRED OPTIONS TO BE SET:
		--folder
	"""
	valid = glob.glob(args.folder)
	skip = glob.glob('/*/*otf.tif*') #skips both .tif and .tiff
	
	for tiff in valid:
		if tiff not in skip:
			process_tiff(tiff, args)
	
def main(args):
	"""sets up the destination folder for processed images, other functionality requires at least one option to be set
	"""
		
	if args.destination is not None:
		os.makedirs(f"{args.destination}/pycudadecon_output", exist_ok=True)
		args.destination = f"{args.destination}/pycudadecon_output"
	else:
		os.makedirs("pycudadecon_output", exist_ok=True)
		args.destination = "pycudadecon_output"
		
	if args.psf is not None:
		make_otf(args.psf, "pycudadecon_output/otf.tif", dzpsf=args.otf_z, dxpsf=args.otf_xy)
		
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
	parser.add_argument('-o', '--otf')
	parser.add_argument('-j', '--json')
	parser.add_argument('--deskew', action='store_true', help='if set, program will assume files have already been deskewed')
	parser.add_argument('--keep_deskew', action='store_true', help='if set, program will also save the deskewed image before deconvolution')
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

