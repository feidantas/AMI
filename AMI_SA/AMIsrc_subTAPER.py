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
#make tapered image with subtraction
# find A376 viral radius; 
# work out the angular size of the viral radius; 
# specify taper in arcminutes

print "Making an subtracted image of "+target+" SA field: clean() --> "+datadir+target+"_im_subtracted_taper1arcm.*"
os.system('rm -rf '+datadir+target+'_im_subtracted_gaussian_taper1arcm.* \n')
default(clean)
clean(vis=visname2, \
	imagename=datadir+target+"_im_subtracted_gaussian_taper1arcm", \
	spw='', \
	field='', \
	mode='mfs',\
	niter=0, \
	imsize=512, \
	interactive=False, \
	threshold = '0.0mJy', \
	mask=[''], \
	multiscale=[], \
	nterms=1, \
	cell='4arcsec', \
	stokes='I', \
	weighting='natural', \
	robust=0.0, \
	gridmode='', \
	uvrange='', \
	uvtaper=True, \
	outertaper=['1arcmin'], \
	usescratch=False)


print "Making an subtracted image of "+target+" SA field: clean() --> "+datadir+target+"_im_subtracted_taper2arcm.*"
os.system('rm -rf '+datadir+target+'_im_subtracted_gaussian_taper2arcm.* \n')
default(clean)
clean(vis=visname2, \
	imagename=datadir+target+"_im_subtracted_gaussian_taper2arcm", \
	spw='', \
	field='', \
	mode='mfs',\
	niter=0, \
	imsize=512, \
	interactive=False, \
	threshold = '0.0mJy', \
	mask=[''], \
	multiscale=[], \
	nterms=1, \
	cell='4arcsec', \
	stokes='I', \
	weighting='natural', \
	robust=0.0, \
	gridmode='', \
	uvrange='', \
	uvtaper=True, \
	outertaper=['2arcmin'], \
	usescratch=False)


print "Making an subtracted image of "+target+" SA field: clean() --> "+datadir+target+"_im_subtracted_taper3arcm.*"
os.system('rm -rf '+datadir+target+'_im_subtracted_gaussian_taper3arcm.* \n')
default(clean)
clean(vis=visname2, \
	imagename=datadir+target+"_im_subtracted_gaussian_taper3arcm", \
	spw='', \
	field='', \
	mode='mfs',\
	niter=0, \
	imsize=512, \
	interactive=False, \
	threshold = '0.0mJy', \
	mask=[''], \
	multiscale=[], \
	nterms=1, \
	cell='4arcsec', \
	stokes='I', \
	weighting='natural', \
	robust=0.0, \
	gridmode='', \
	uvrange='', \
	uvtaper=True, \
	outertaper=['3arcmin'], \
	usescratch=False)


print "Making an subtracted image of "+target+" SA field: clean() --> "+datadir+target+"_im_subtracted_taper4arcm.*"
os.system('rm -rf '+datadir+target+'_im_subtracted_gaussian_taper4arcm.* \n')
default(clean)
clean(vis=visname2, \
	imagename=datadir+target+"_im_subtracted_gaussian_taper4arcm", \
	spw='', \
	field='', \
	mode='mfs',\
	niter=0, \
	imsize=512, \
	interactive=False, \
	threshold = '0.0mJy', \
	mask=[''], \
	multiscale=[], \
	nterms=1, \
	cell='4arcsec', \
	stokes='I', \
	weighting='natural', \
	robust=0.0, \
	gridmode='', \
	uvrange='', \
	uvtaper=True, \
	outertaper=['4arcmin'], \
	usescratch=False)

print "Making an subtracted image of "+target+" SA field: clean() --> "+datadir+target+"_im_subtracted_taper5arcm.*"
os.system('rm -rf '+datadir+target+'_im_subtracted_gaussian_taper5arcm.* \n')
default(clean)
clean(vis=visname2, \
	imagename=datadir+target+"_im_subtracted_gaussian_taper5arcm", \
	spw='', \
	field='', \
	mode='mfs',\
	niter=0, \
	imsize=512, \
	interactive=False, \
	threshold = '0.0mJy', \
	mask=[''], \
	multiscale=[], \
	nterms=1, \
	cell='4arcsec', \
	stokes='I', \
	weighting='natural', \
	robust=0.0, \
	gridmode='', \
	uvrange='', \
	uvtaper=True, \
	outertaper=['5arcmin'], \
	usescratch=False)

print "Making an subtracted image of "+target+" SA field: clean() --> "+datadir+target+"_im_subtracted_taper6arcm.*"
os.system('rm -rf '+datadir+target+'_im_subtracted_gaussian_taper6arcm.* \n')
default(clean)
clean(vis=visname2, \
	imagename=datadir+target+"_im_subtracted_gaussian_taper6arcm", \
	spw='', \
	field='', \
	mode='mfs',\
	niter=0, \
	imsize=512, \
	interactive=False, \
	threshold = '0.0mJy', \
	mask=[''], \
	multiscale=[], \
	nterms=1, \
	cell='4arcsec', \
	stokes='I', \
	weighting='natural', \
	robust=0.0, \
	gridmode='', \
	uvrange='', \
	uvtaper=True, \
	outertaper=['6arcmin'], \
	usescratch=False)

print "Making an subtracted image of "+target+" SA field: clean() --> "+datadir+target+"_im_subtracted_taper7arcm.*"
os.system('rm -rf '+datadir+target+'_im_subtracted_gaussian_taper7arcm.* \n')
default(clean)
clean(vis=visname2, \
	imagename=datadir+target+"_im_subtracted_gaussian_taper7arcm", \
	spw='', \
	field='', \
	mode='mfs',\
	niter=0, \
	imsize=512, \
	interactive=False, \
	threshold = '0.0mJy', \
	mask=[''], \
	multiscale=[], \
	nterms=1, \
	cell='4arcsec', \
	stokes='I', \
	weighting='natural', \
	robust=0.0, \
	gridmode='', \
	uvrange='', \
	uvtaper=True, \
	outertaper=['7arcmin'], \
	usescratch=False)



end = timer()
length = end - begin

print "Imaging took ",length," sec"




