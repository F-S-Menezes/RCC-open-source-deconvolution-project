from pathlib import Path
import numpy as np
from skimage.io import imsave,imread
import os

from pycudadecon.affine import affineGPU, deskewGPU
#from pycudadecon.util import imread

def main(im_path):
	"test that we can actually deskew an image"
	im=imread(str(im_path))

	im_z, im_y, im_x =im.shape
#	TMAT = np.array([[1, 0, 0, im_x], [0, 1, 0, im_y], [0, 0, 1, im_z], [0, 0, 0, 1]])
	
#	out = affineGPU(im, TMAT)
	out = deskewGPU(im)
	
	dirname, fname = os.path.split(im_path)
	fname, ext = os.path.splitext(fname)
	outdir = os.path.join(dirname, fname + "_deskewed")
	os.makedirs(outdir, exist_ok=True)
	dst = os.path.join(outdir, f"{im_path}_deskewed.tif")
	
#	print(outdir)
#	print(dst)
#	print(fname)
#	print(im_path)
#	print(im.shape)
	
	imsave(dst, out, imagej=True)
	
	
	
if __name__ == "__main__":
    import sys

    main(sys.argv[1])
