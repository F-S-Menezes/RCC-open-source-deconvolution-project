# RCC-open-source-deconvolution-project 
This project provides two {singularity}(https://sylabs.io/guides/3.9/user-guide/) definition files and one program file for implementing {pycudadecon}(https://github.com/tlambert03/pycudadecon) as an open source option for the UQ image-processing portal. Also contains a json file and batch file for testing purposes (more below)

##Using the singularity defintion files (conda_base.def and nvidia_base.def)
Both singularity definiton files can be built either locally using the command below (substituting XXXX for the desired base, version should not matter but testing was done with version 3.9.0-rc.3) or via the (sylabs remote builder){https://cloud.sylabs.io/builder}.

'''sh
sudo singularity build XXXX_base.sif XXXX_base.def
'''

To run either base requires a full installation of singularity (any version). Be sure to run them using the --nv option in order to use cuda libraries.

example
'''sh
singularity exec --nv conda_base.sif nvidia-smi
'''

##Using process.py

The main program {process.py}(https://github.com/F-S-Menezes/RCC-open-source-deconvolution-project/blob/main/process.py) runs at the command-line and requires one or more options to be set for any real functionality. These options can be split into functions and arguments, functions take a file or files and perform some form of processing, arguments allow you to change some of the default behaviour of this processing. Every call to this function will create a 'pycudadecon\_output' folder and put __all__ created files in that folder (unless a 'pycudadecon_output' folder already exists)

###Arguments

-o, --otf: takes a path to a pre-generated otf file to be used for deconvolution

--deskew: if set, program will assume files have already been deskewed

--keep\_deskew: if set, program will also save the deskewed image before deconvolution

-d, --destination: takes a file path and allows the destination folder of processed images to be something other than $PWD/pycudadecon\_output/

--dxdata: int of the XY pixel size of the data

--dzdata: int of the data's pixel depth

--angle: int angle of the microscope

--otf\_xy: int XY pixel size of the psf file

--otf\_z: int psf file pixel depth

--background: int average background value to subtract for deconvolution

###Functions

-p, --psf: takes a path to a psf file and generates an otf file, if created in the same call as another operation that requires an otf file, that operation will use this created otf file (overides --otf)

-t, --files: takes one or more paths to tiff file/s and processes them

-f, --folder: takes the form path\_to\_folder/pattern, where path\_to\_folder is simply the path to the source folder containing images to be processed, and pattern is a unix-style search expression. utilizes (glob){https://docs.python.org/3/library/glob.html}

-j, --json: takes a json of the same or similar form as (test\_json.json){https://github.com/F-S-Menezes/RCC-open-source-deconvolution-project/blob/main/test\_json.json} and uses the information contained within to set arguments as needed. A single json is equivalent to a commandline execution of this program with __either__ -t or -f set, not both.

##Trouble-shooting
cudaSetDevice() error, This is the most likely issue you might encounter, it means that cuda can not detect the necessary driver files. This is a host machine issue. (Check that your graphics driver is cuda-capable){https://developer.nvidia.com/cuda-gpus}, check that running \'nvidia-smi\' returns something (that is, succesful output will look a table, unsuccesful output will not run), and/or re-install your nvidia driver.

ValueError: not enough values to unpack (expected 3, got 2), if you get this error when attempting to generate an otf from a psf file, there is something faulty with the psf file

write failed because no space left on device, this can occur whilst building the definition file on a local machine with insufficiant memory. Consider building using the (sylabs remote builder){https://cloud.sylabs.io/builder}






