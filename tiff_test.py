from pathlib import Path
import numpy as np
from skimage.io import imsave,imread
import os

from pycudadecon.affine import deskewGPU
from pycudadecon import decon, rl_cleanup, rl_decon, rl_init, make_otf
#from pycudadecon.util import imread

class Process:
	"""class structure to aid with functions that deskew and/or deconvolve some .tif/.tiff image
	"""
	
	def __init__(self, im_path, psf=None):
		"""initializes some frequently used properties
	
		Params:
			im_path (string): path to the image
			mode (bool): 0 to only deskew the image or 1 to also deconvolve it, saves seperately
		"""
		self._im_path = im_path
		self._im = imread(str(im_path))
		self._psf = psf
		self._otf = None
		dirname, self._fname = os.path.split(im_path) #the original filename, that spawned files will piggy-back their names off of
		self._fname, ext = os.path.splitext(self._fname)
		self._outdir = os.path.join(dirname, self._fname + "_pycudadecon")
		os.makedirs(self._outdir, exist_ok=True)
		
	def run(self):
	
		deskewed = deskewGPU(self._im)
	
		if self._psf is not None:
			print("\ngenerating otf")
			make_otf(self._psf, f"{self._outdir}/{self._fname}_otf.tiff")
			
			print("deconvolving image")
			rl_init(deskewed.shape, f"{self._outdir}/{self._fname}_otf.tiff", ) 
			deconvolved = rl_decon(deskewed, background='auto')
			self.save_file(deconvolved, "deconvolved")
			rl_cleanup()
		else:
			print("deskew only")
			self.save_file(deskewed, "deskewed")
			
	
	def save_file(self, out, save_as):
		"""saves the file 'out' to the pycudadecon folder of this process

		PARAMETERS:
			out (numpy.ndarray): an image processed by pycudadecon to be saved
			save_as(string): what to name the given file
		"""
		dst = os.path.join(self._outdir, f"{self._fname}_{save_as}.tiff")
		imsave(dst, out, imagej=True)

def main(args):
	"""test deskew and/or deconvolve
	
	PARAMETERS:
	im_path (string): path to the image
	decon (bool): 0 to only deskew the image or 1 to also deconvolve it, saves seperately
	"""
	if len(args)>2 or len(args)==0:
		print("WARNING: incorrect number of args\nusage:\nto deskew:\tpython3 tiff_xxxx raw_file.tif/tiff\nto deconvolve:\tpython3 tiff_xxxx raw_file.tif/tiff instrument_psf.tif/tiff")
	print("\nspacing\n")
	
	im_path = args[0]
	if len(args)>1:
		psf_path = args[1]
		data = Process(im_path, psf_path)
	else:
		data = Process(im_path)

	data.run()
	
if __name__ == "__main__":
	import sys

	main(sys.argv[1:])
