import os,sys

from timeit import default_timer as timer

runclean=True

begin = timer()


if runclean:
	os.system('rm -rf ../DATA/*  \n')
	os.system('rm -rf ../CALIBRATION/*  \n')

execfile('load_data.py')
execfile('flag_data.py')
execfile('calibrate_data.py')
execfile('image_LA_fields.py')
os.system('rm -rf *_LA-FLATN.FITS')
os.system('mv ../DATA/*-UV.FITS  ../SCRIPTS/  \n')
os.system('sh flatn_*.sh  \n')
#in PyBDSF
execfile('run_pybdsm.py')
#in CASAPy

execfile('pybdsm2ann.py')
execfile('pybdsm2cl_ATT_gaussian.py')

os.system('rm -rf casa*.log \n')
os.system('rm -rf ipython*.log \n')
os.system('rm -rf *.last \n')

end = timer()

print "This script took ",end-begin," sec"

