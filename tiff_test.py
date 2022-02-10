from pathlib import Path
import numpy as np
from skimage.io import imsave,imread
import os

from pycudadecon.affine import affineGPU, deskewGPU
from pycudadecon import decon, rl_cleanup, rl_decon, rl_init
#from pycudadecon.util import imread

class Testing:
	"""class structure to aid with functions that deskew and/or deconvolve some .tif/.tiff image
	"""
	
	def __init__(self, im_path, mode):
		"""initializes some frequently used properties
	
		Params:
			im_path (string): path to the image
			mode (bool): 0 to only deskew the image or 1 to also deconvolve it, saves seperately
		"""
		self._im_path = im_path
		self._mode = mode
		self._im = imread(str(im_path))
		dirname, self._fname = os.path.split(im_path) #the original filename that spawned files will piggy-back their names off of
		self._fname, ext = os.path.splitext(self._fname)
		self._outdir = os.path.join(dirname, self._fname + "_pycudadecon")
		os.makedirs(self._outdir, exist_ok=True)
		
	def run(self):
		#	im_z, im_y, im_x =im.shape
#		TMAT = np.array([[1, 0, 0, im_x], [0, 1, 0, im_y], [0, 0, 1, im_z], [0, 0, 0, 1]])
	
#		out = affineGPU(im, TMAT)
		out = deskewGPU(self._im)
		self.save_file(out)
	
#		if self._mode:
#			rl_init(deskewed.shape, im_path) 
#			print(deskewed.shape)
#			out = rl_decon(deskewed, background=100)
#			self.save_file(out, im_path, outdir)
#			rl_cleanup()
	
	def save_file(self, out):
		"""saves the file im to a   new folder and returns the path to the saved file.

		PARAMETERS:
			im (imread object): the file to be saved
			im_path (string): path to the image to be saved
			outdir (string): used when deconvolving so that we reuse the same folder created when saving the deskewed image
		"""
		if self._mode == 1:
			dst = os.path.join(self._outdir, f"{self._fname}_deconvolved.tiff")
		else:
			dst = os.path.join(self._outdir, f"{self._fname}_deskewed.tiff")
		imsave(dst, out, imagej=True)
#		return(outdir, new_file)

def main(im_path, mode):
	"""test deskew and/or deconvolve
	
	PARAMETERS:
	im_path (string): path to the image
	decon (bool): 0 to only deskew the image or 1 to also deconvolve it, saves seperately
	"""
	data = Testing(im_path, mode)
	data.run()
	
if __name__ == "__main__":
	import sys
	
#	print(sys.argv[1])
#	print(sys.argv[2])
	main(sys.argv[1], sys.argv[2])
