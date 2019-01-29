import numpy as np
from timeit import default_timer as timer

execfile("/home/fdantas/mytasks/mytasks.py")

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

cal_obs = '3C286'
cal_sec = 'J0256+1334'
target = 'A399'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

datadir = '../DATA/'
visname = datadir+target+".ms"
msfits = datadir+target+"-UV.FITS" 
aipsname = datadir+target+"_LA-FLATN.FITS"
casaname = datadir+target+"_LA-FLATN"
aipsdir = '/raid/scratch/fdantas/Clarke_Clusters/A399_new/CLARKE_LA/160912/SCRIPTS'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

# Optional steps:
imag1 = False   # make CASA image for each field
expt1 = True    # export MS into FITS files for FLATN in AIPS
aips1 = True   # make AIPS script for FLATN
aips2 = True   # run AIPS script
impt1 = True   # convert AIPS output to CASA image

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


begin = timer()

msmd.open(visname)
nfield=msmd.nfields()
msmd.close()

print "There are "+str(nfield)+" fields"

if imag1:
	for i in range(0,nfield):

		imname = target+"_F"+str(i)
		print "Making an image of "+target+" field "+str(i)+" : clean()"
		os.system('rm -rf '+datadir+target+"_F"+str(i)+'.* \n')
		default(clean)
		clean(vis=visname, \
			imagename=datadir+target+"_F"+str(i), \
			spw='', \
			field=str(i), \
			mode='mfs',\
			niter=0, \
			imsize=256, \
			cell='4.5arcsec', \
			interactive=False )


if expt1:
	print "Exporting UV fits from CASA: exportuvfits() --> "+datadir+target+"-UV.FITS"
	os.system('rm -rf '+datadir+target+'-UV.FITS \n')
	default(exportuvfits)
	exportuvfits(vis= visname, fitsfile = msfits, datacolumn = 'corrected')
	
if aips1:
	print "Making bash script for AIPS FLATN: flatn_"+target+".sh"
	filename = "flatn_"+target+".sh"
	bfile = open('tmp.sh','w')
	bfile.write("#!/bin/sh \n\n\n\n")
	bfile.write("msfits='PWD:"+target+"-UV.FITS' \n")
	bfile.write("myname='"+target+"_LA'  \n")
	bfile.write("outname='PWD:"+target+"_LA-FLATN.fits'  \n")
	bfile.write("phasecnt='02,57,50.000, +13,03,16.461'  \n")
	bfile.write("nfield="+str(nfield)+"  \n")
	bfile.write("imsize1=256  \n")
	bfile.write("imsize2=512  \n")
	bfile.write("cell=4.5  \n")
	bfile.close()

	os.system("cat tmp.sh aips_template.sh > "+filename+"  \n")
	

if aips2:
	os.system('export AIPSDATA="'+aipsdir+'" \n')
	os.system('rm -rf '+aipsname+'  \n')
	os.system('sh flatn_'+target+'.sh > '+target+'_aips.log \n')

if impt1:
	importfits(fitsimage = aipsname, imagename = casaname, overwrite=True)
	

end = timer()
length = end - begin

print "Imaging took ",length," sec"



