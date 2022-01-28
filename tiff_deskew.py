from pathlib import Path
import numpy as np
from skimage.io import imsave
import os

from pycudadecon.affine import affineGPU
from pycudadecon.util import imread

def main(im_path):
	"test that we can actually deskew an image"
	im=imread(str(im_path))
	
	out = affineGPU(im, np.eye(4))
	
	dirname, fname = os.path.split(im_path)
	fname, ext = os.path.splitext(fname)
	outdir = os.path.join(dirname, fname + "_deskewed")
	os.makedirs(outdir, exist_ok=True)
	dst = os.path.join(outdir, f"{im_path}_deskewed.tif")
	
	imsave(dst, out, imagej=True)
	
	
if __name__ == "__main__":
    import sys

    main(sys.argv[1])
