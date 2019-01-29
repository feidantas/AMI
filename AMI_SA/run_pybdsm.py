import numpy as np
from timeit import default_timer as timer

begin = timer()

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

cal_obs = '3C286'
cal_sec = 'J0042+2320'
target = 'A75'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

datadir = '../DATA/'
aipsname = datadir+target+"_LA-FLATN.FITS"
casaname = datadir+target+"_LA-FLATN"

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

os.system('source /lofar/lofar-2_19/SL7/lofar/release/lofarinit.csh \n')
os.system('source /lofar/lofar-2_19/SL7/init_env_release.csh  \n')

print "Making bash script for PYBDSM: target+"_pybdsm.sh"
filename = target+"_pybdsm.sh"

bfile = open('tmp.sh','w')
bfile.write("#!/bin/sh \n\n\n\n")
bfile.write("infile="+datadir+aipsname+" \n")
bfile.write("outfile="+datadir+casaname+".csv  \n")
bfile.close()

os.system("cat tmp.sh pybdsm_template.sh > "+filename+"  \n")
os.system('sh pybdsm_'+target+'.sh > '+target+'_pybdsm.log \n')

end = timer()
length = end - begin

print "This script took ",length," sec"



