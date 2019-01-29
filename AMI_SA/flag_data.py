import numpy as np
from timeit import default_timer as timer

begin = timer()

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

cal_obs = '3C286'
cal_sec = 'J0309+1029'
target = 'A399'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

visname = '../DATA/'+target+'_fxd.MS'	# 'fxd' = 'scan numbers fixed'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

datadir = '../DATA/'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

nchan = 2048
nspw = 2
flagtime=qa.quantity('5min')

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

msmd.open(visname)
nant=msmd.nantennas()
nspw=msmd.nspw()
nchan_vis=msmd.nchan(0)
bin_fact=nchan/nchan_vis
tr=msmd.timerangeforobs(0)
obs_len=qa.sub(tr['end']['m0'],tr['begin']['m0']) # observation length as a quantity
mywinsize=int(round(qa.div(obs_len, qa.convert(flagtime, qa.unit(obs_len)))['value']))
mywinsize=max(mywinsize, 1)
baselines=msmd.baselines()
msmd.close()

# ---------------------------------------------------------------------------------------

# flag visibilities with zero weight:
if not os.path.exists(visname+'.flagversions/flags.flagdata_1'):
	print "===>flagging zero weight data"
	flagdata(vis=visname,\
			field='',\
			mode='clip',\
			datacolumn='weight_spectrum', \
			clipzeros=True, \
			action='apply', \
			display='none', \
			flagbackup=True)

# flag visibilities affected by shadowing:
if not os.path.exists(visname+'.flagversions/flags.flagdata_2'):
	print "===>flagging shadowed data"
	flagdata(vis=visname, mode='shadow', flagbackup=True)


mywinsize=int(round(qa.div(obs_len, qa.convert(flagtime, qa.unit(obs_len)))['value']))
print "===>baseline based flagging"
for i in range(nant-1):
	for j in range(i+1, nant):
		if not baselines[i,j]: continue 
                flagdata(vis=visname, mode='rflag', ntime='scan', combinescans=False,\
				datacolumn='data', winsize=mywinsize, timedevscale=10.,\
				freqdevscale=10., action='apply', display='', flagbackup=False,\
				antenna=str(i)+'&'+str(j))
            

print "===>flagging strong narrow band RFI"
flagdata(vis=visname, mode='rflag', ntime='scan', combinescans=False,\
		datacolumn='data', winsize=mywinsize, timedevscale=5.,\
		freqdevscale=5., action='apply', display='', flagbackup=False)


new_bin_fact=64
print "===>averaging to 64 channels"
split(vis=visname, outputvis=datadir+target+'_avg.MS', datacolumn='data', width=new_bin_fact/bin_fact)

os.system('mv '+visname+' '+datadir+cal_obs+'_fullres.ms')
os.system('mv '+visname+'.flagversions '+datadir+cal_obs+'_fullres.ms.flagversions')
os.system('mv '+datadir+target+'_avg.MS '+visname)

print "===>flagging averaged data 1"
flagdata(vis=visname, mode='rflag', ntime='scan', combinescans=False,\
		datacolumn='data', winsize=mywinsize, timedevscale=5.,\
		freqdevscale=5., action='apply', display='', flagbackup=False)
     
print "===>flagging averaged data 2"
flagdata(vis=visname, mode='rflag', ntime='scan', combinescans=False, datacolumn='data',\
		winsize=1, timedevscale=5., freqdevscale=5., action='apply', display='',\
		flagbackup=False, channelavg=True, chanbin=2)
     


# fix state_ids to -1 to avoid errors due to missing STATE table
tb.open(visname, nomodify=False)
nrows=tb.nrows()
tb.putcol(columnname='STATE_ID', value=-1*np.ones((nrows)))
tb.unlock()
tb.close()

end = timer()

print "Flagging took ",end-begin," sec"


