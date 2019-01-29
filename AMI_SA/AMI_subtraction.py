import numpy as np
import time
import shutil
from timeit import default_timer as timer

begin = timer()

execfile("/home/fdantas/mytasks/mytasks.py")

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

cal_obs = '3C286'
cal_sec = 'J0309+1029'
target = 'A399'

 #---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

datadir = '../DATA/'

caldir = datadir

visname2 = datadir+target+".ms"	# 'fxd' = 'scan numbers fixed'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


COMP_LIST = datadir+target+'_LA-FLATN.cl'

#clearcal(vis = visname2)

#FT task
print ">>>>FT task over Original MS"
default('ft')
ft(vis = visname2, \
	field = '', \
	spw ='', \
	usescratch = True, \
	incremental = False, \
	model='', \
	complist = COMP_LIST)

#UVSUB task

print " Subtracting Original MS"
default('uvsub')
uvsub(vis = visname2, \
	reverse = False)








print "Making an subtracted image of "+target+" SA field: clean() --> "+datadir+target+"_im_subtracted.*"
os.system('rm -rf '+datadir+target+'_im_subtracted.* \n')
default(clean)
clean(vis=visname2, \
	imagename=datadir+target+"_im_subtracted", \
	spw='', \
	field='', \
	mode='mfs',\
	niter=0, \
	imsize=512, \
	cell='4arcsec', \
	interactive=False )


end = timer()
length = end - begin

print "Imaging took ",length," sec"



