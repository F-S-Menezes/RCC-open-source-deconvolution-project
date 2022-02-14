from pathlib import Path
import numpy as np
from skimage.io import imsave,imread
import os

from pycudadecon.affine import affineGPU, deskewGPU
from pycudadecon import decon, rl_cleanup, rl_decon, rl_init
#from pycudadecon.util import imread

class Process:
	"""class structure to aid with functions that deskew and/or deconvolve some .tif/.tiff image
	"""
	
	def __init__(self, im_path, psf_path=None):
		"""initializes some frequently used properties
	
		Params:
			im_path (string): path to the image
			mode (bool): 0 to only deskew the image or 1 to also deconvolve it, saves seperately
		"""
		self._im_path = im_path
		self._im = imread(str(im_path))
		self._psf_path = psf_path
		self._otf = None
#		dirname, self._fname = os.path.split(im_path) #the original filename, that spawned files will piggy-back their names off of
#		self._fname, ext = os.path.splitext(self._fname)
#		self._outdir = os.path.join(dirname, self._fname + "_pycudadecon")
#		os.makedirs(self._outdir, exist_ok=True)
		
	def run(self):
	
		out = deskewGPU(self._im)
		print("wtf is this: ", type(out))
#		self.save_file(out)
	
		if self._psf_path is not None:
			print("decon")
			########working on this section
#			rl_init(deskewed.shape, im_path) 
#			print(deskewed.shape)
#			out = rl_decon(deskewed, background=100)
#			self.save_file(out, im_path, outdir)
#			rl_cleanup()
		else:
			print("deskew only")
	
	def save_file(self, out):
		"""saves the file 'out' to the pycudadecon folder of this process

		PARAMETERS:
			out (numpy.ndarray): an image processed by pycudadecon to be saved
		"""
		if self._psf is not None:
			dst = os.path.join(self._outdir, "otf.tiff")
		else if self._otf is not None:
			dst = os.path.join(self._outdir, f"{self._fname}_deconvolved.tiff")
		else:
			dst = os.path.join(self._outdir, f"{self._fname}_deskewed.tiff")
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
