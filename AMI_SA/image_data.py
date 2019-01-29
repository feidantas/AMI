import numpy as np
from timeit import default_timer as timer

execfile("/home/fdantas/mytasks/mytasks.py")

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

cal_obs = '3C286'
cal_sec = 'J0309+1029'
target = 'A399'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

datadir = '../DATA/'
visname = datadir+target+".ms"
msfits = datadir+target+"-uv.fits" 

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

# Optional steps:
imag1 = True   # make CASA image for field

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


begin = timer()

if imag1:

	print "Making an image of "+target+" SA field: clean() --> "+datadir+target+"_im.*"
	os.system('rm -rf '+datadir+target+'_im.* \n')
	default(clean)
	clean(vis=visname, \
		imagename=datadir+target+"_im", \
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



