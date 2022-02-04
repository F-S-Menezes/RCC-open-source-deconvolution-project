from pathlib import Path
from skimage.io import imsave,imread
import os

from pycudadecon.affine import deskewGPU

def main(im_path):
	"test that we can actually deskew an image"
	im=imread(str(im_path))

	out = deskewGPU(im)
	
	dirname, fname = os.path.split(im_path)
	fname, ext = os.path.splitext(fname)
	outdir = os.path.join(dirname, fname + "_deskewed")
	os.makedirs(outdir, exist_ok=True)
	dst = os.path.join(outdir, f"{im_path}_deskewed.tif")
		
	imsave(dst, out, imagej=True)
	
	
	
if __name__ == "__main__":
    import sys

    main(sys.argv[1])
