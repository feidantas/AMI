import os,sys
import numpy as np
from timeit import default_timer as timer

begin = timer()

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

cal_obs = '3C286'
cal_sec = 'J0256+1334'
target = 'A399'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

datadir = '../DATA/'
aipsname = target+"_LA-FLATN.FITS"
casaname = target+"_LA-FLATN"

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

os.system('source /lofar/lofar-2_19/SL7/lofar/release/lofarinit.csh \n')
os.system('source /lofar/lofar-2_19/SL7/init_env_release.csh  \n')

print "Making bash script for PYBDSM: --> "+target+"_pybdsm.sh"
filename = target+"_pybdsm.sh"

bfile = open('tmp.sh','w')
bfile.write("#!/bin/sh \n\n\n\n")
bfile.write("infile="+aipsname+" \n")
bfile.write("outfile="+casaname+".csv  \n")
bfile.close()

os.system('rm -rf '+casaname+".csv  \n")
os.system("cat tmp.sh pybdsm_template.sh > "+filename+"  \n")
os.system('sh '+target+'_pybdsm.sh > '+target+'_pybdsm.log \n')
os.system('rm -rf tmp.sh  \n')

end = timer()
length = end - begin

print "This script took ",length," sec"



