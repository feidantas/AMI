import os,sys
from timeit import default_timer as timer

runclean=False

begin = timer()

#if runclean:
	#os.system('rm -rf ../DATA/*  \n')
	#os.system('rm -rf ../CALIBRATION/*  \n')

#execfile('load_data.py')
#execfile('flag_data.py')
#execfile('calibrate_data.py')
#execfile('image_data.py')
#os.system('mv ../../../CLARKE_LA/160912/SCRIPTS/*.cl  ../DATA/  \n')
#execfile('AMI_flag_2.py')
execfile('AMI_subtraction.py')


os.system('rm -rf casa*.log \n')
os.system('rm -rf ipython*.log \n')
os.system('rm -rf *.last \n')

end = timer()

print "Full script took ",end-begin," sec"

