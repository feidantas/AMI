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

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

visname = '../DATA/'+target+'_fxd.MS'	# 'fxd' = 'scan numbers fixed'
oldvis = '../DATA/'+target+'_old.MS'	# 'fxd' = 'scan numbers fixed'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

datadir = '../DATA/'
caldir = '../CALIBRATION/'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

targ = '0'	# A119 : Target Field
pcal = '2'	# 3C286 : Primary Calibrator
scal = '1'	# J0042+2320 : Secondary Calibrator

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

# Reference antenna:
REF = '1'   # SA1

# Frequency stuff:
SPW = ''

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

# Calibration stuff:
setjyAMI = False
gain1 = True 	# initial phase calibration
delay = True 	# delay calibration
bndps = True 	# bandpass calibration
gain2 = True	# complex gain calibration on primary
chck1 = True	# make check maps
flag1 = True	# flag secondary before gaincal
gain3 = True    # phase and amp on phase calibrator
flux1 = True    # bootstrap fluxes
chck2 = True    # make check maps
acal1 = True    # apply calibration to target

doplot= True 	# output plots of cal solutions

# check for data:
if os.path.exists(oldvis):
	os.system('rm -rf '+visname+'  \n')
	os.system('cp -r '+oldvis+' '+visname+'  \n')
else:
	# make a backup copy:
	os.system('cp -r '+visname+' '+oldvis+' \n')


# fix state_ids to -1 to avoid errors due to missing STATE table
tb.open(visname, nomodify=False)
nrows=tb.nrows()
tb.putcol(columnname='STATE_ID', value=-1*np.ones((nrows)))
tb.unlock()
tb.close()

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#		
#			                     CALIBRATOR REDUCTION
#
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# --------------------------------------
# set the flux scale:
if not setjyAMI:
    print "Setting the flux scale: setjy()"
    setjy(vis=visname, \
		field=pcal, \
		standard='Perley-Butler 2013')
else:
    print "Setting the flux scale: setjy_ami()"
    fluxpars=setjy_ami(vis=visname, do_plots=False)
    setjy(vis=visname, \
		  field=fluxpars['field'], \
		  standard='manual', \
		  fluxdensity=fluxpars['fluxdensity'], \
		  spix=fluxpars['spix'][0], \
		  reffreq=fluxpars['reffreq'])


# --------------------------------------
# initial phase cal:\

bin_fact = 64
chan1=1526/bin_fact
chan2=max(1546/bin_fact, chan1+1)
chan1=str(chan1)
chan2=str(chan2)
#print bin_fact, chan1, chan2

if gain1:
	print "Doing initial phase calibration: gaincal() --> G0"
	caltab = caldir+'G0-'+cal_obs
	if os.path.exists(caltab): rmtables(caltab)
	gaincal(vis=visname, \
			field=pcal, \
			caltable=caltab, \
			solint='120s', \
			spw='0:'+chan1+'~'+chan2+',1:'+chan1+'~'+chan2, \
			refant=REF, \
			minblperant=1, \
			minsnr=2., \
			solnorm=False, \
			gaintype='G', \
			calmode='p')


# --------------------------------------
# delay calibration:
if delay:
	print "Doing delay calibration: gaincal() --> K0"
	caltab = caldir+'K0-'+cal_obs
	if os.path.exists(caltab): rmtables(caltab)
	gaincal(vis=visname, \
			field=pcal, \
			caltable=caltab, \
			solint='inf', \
			minblperant=1, \
			minsnr=3.0, \
			refant=REF, \
			gaintype='K', \
			spw=SPW, \
			gaintable=[caldir+'G0-'+cal_obs], \
			solnorm=False) 



# --------------------------------------
# bandpass calibration:
if bndps:
	print "Doing bandpass calibration: bandpass() --> B0"
	caltab = caldir+'B0-'+cal_obs
	if os.path.exists(caltab): rmtables(caltab)
	bandpass(vis=visname, \
			field=pcal, \
			caltable=caltab, \
			solint='inf', \
			minblperant=1, \
			minsnr=0.0, \
			refant=REF, \
			bandtype='B', \
			spw=SPW, \
			gaintable=[caldir+'G0-'+cal_obs,caldir+'K0-'+cal_obs], \
			solnorm=False, \
			fillgaps=0) 



# --------------------------------------
# gain calibration:
if gain2:
	print "Doing gain calibration: gaincal() --> G1"
	caltab = caldir+'G1-'+cal_obs
	if os.path.exists(caltab): rmtables(caltab)
	gaincal(vis=visname, \
			field=pcal, \
			caltable=caltab, \
			solint='120s', \
			minblperant=3, \
			minsnr=3.0, \
			refant=REF,\
			calmode='ap',  \
			gaintable=[caldir+'K0-'+cal_obs,caldir+'B0-'+cal_obs], \
			gaintype='G')


# --------------------------------------
# make a map to check the imaging:
if chck1:
	print "Applying calibration: applycal()"
	applycal(vis=visname, \
			field=pcal, \
			gaintable=[caldir+'K0-'+cal_obs, caldir+'B0-'+cal_obs, caldir+'G1-'+cal_obs], \
			interp=['nearest','nearest','linear'], \
			calwt=[False,False,False], \
			parang=False, \
			flagbackup=True)


	print "Doing a bit of flagging on primary: flagdata()"
	flagdata(vis=visname, \
			mode='rflag', \
			datacolumn='corrected', \
			action='apply', \
			display='none' )



	print "Making a dirty image: clean() --> "+cal_obs+".image"
	os.system('rm -rf '+datadir+cal_obs+'_im.* \n')
	clean(vis=visname, \
			field=pcal, \
			imagename=datadir+cal_obs+"_im", \
			spw='', \
			mode='mfs',\
			niter=0, \
			imsize=512, \
			cell='4.5arcsec', \
			interactive=False )


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#		
#			                    	TARGET CALIBRATION
#
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


print ''
print ''
print '>>>Beginning calibration of '+target
print ''


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# do some flagging:
if flag1:
	#apply primary solutions to secondary calibrator for flagging
	print "Applying calibration to secondary: applycal()"
	applycal(vis=visname, \
		field=scal,\
		gaintable=[caldir+'K0-'+cal_obs, caldir+'B0-'+cal_obs,caldir+'G1-'+cal_obs], \
		gainfield=[pcal,pcal,pcal], \
		interp=['nearest','nearest','nearest'],\
		calwt=[False,False,False], \
		parang=False, \
		flagbackup=True)

	print "Doing a bit of flagging on secondary: flagdata()"
	flagdata(vis=visname, \
			field=scal, \
			mode='rflag', \
			datacolumn='corrected', \
			action='apply', \
			display='none' )
		
	print "clearing calibrations: clearcal()"
	clearcal(vis=visname, field=scal)


# gain calibration:
if gain3:
    print "Appending secondary complex gain solutions: gaincal() --> G1-"+cal_obs
    caltab = caldir+'G1-'+cal_obs
    #if os.path.exists(caltab): rmtables(caltab)
    gaincal(vis=visname, \
        caltable=caltab, \
        field=scal, \
        combine='obs', \
        solint='120s', \
        minblperant=3, \
        minsnr=0.0, \
        refant=REF,\
        calmode='ap',  \
        gaintable=[caldir+'K0-'+cal_obs,caldir+'B0-'+cal_obs], \
        gainfield=[pcal, pcal], \
        interp=['nearest','nearest'], \
        gaintype='G',\
        append=True)



# transfer flux scale:
if flux1:
  print "Transferring flux scale: fluxscale() --> F1"
  caltab = caldir+'G1-'+cal_obs
  flxtab = caldir+'F1-'+cal_sec
  if os.path.exists(flxtab): rmtables(flxtab)
  myflux = fluxscale(vis=visname,\
        caltable=caltab,\
        fluxtable=flxtab,\
        reference=pcal,\
        transfer=scal)



# make a map to check the imaging:
if chck2:
	print "Applying calibration to secondary: applycal()"
	clearcal(vis=visname, field=scal)
	applycal(vis=visname, \
		field=scal,\
		gaintable=[caldir+'K0-'+cal_obs, caldir+'B0-'+cal_obs,caldir+'F1-'+cal_sec], \
		gainfield=[pcal,pcal,scal], \
		interp=['nearest','nearest','linear'],\
		calwt=[False,False,False], \
		parang=False, \
		flagbackup=True)

	print "Making an image of "+cal_sec+": clean()"
	os.system('rm -rf '+datadir+cal_sec+'_im.* \n')
	default(clean)
	clean(vis=visname, \
		imagename=datadir+cal_sec+'_im', \
		spw='', \
		field=scal, \
		mode='mfs',\
		niter=500, \
		imsize=256, \
		cell='5arcsec', \
		interactive=False )



# apply calibration to target:
if acal1:
	print "Applying calibration to target: applycal()"
	clearcal(vis=visname, field=targ)
	applycal(vis=visname, \
		field=targ,\
		gaintable=[caldir+'K0-'+cal_obs, caldir+'B0-'+cal_obs, caldir+'F1-'+cal_sec], \
		gainfield=[pcal,pcal,scal], \
		interp=['nearest','nearest','linear'],\
		calwt=[False,False,False], \
		parang=False, \
		flagbackup=True)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

bin_width=8
if os.path.exists(datadir+cal_sec+'.ms'): shutil.rmtree(datadir+cal_sec+'.ms')
split(vis=visname, outputvis=datadir+cal_sec+'.ms', field=scal, width=bin_width,datacolumn='corrected')

# fix state_ids to -1 to avoid errors due to missing STATE table
tb.open(datadir+cal_sec+'.ms', nomodify=False)
nrows=tb.nrows()
tb.putcol(columnname='STATE_ID', value=-1*np.ones((nrows)))
tb.unlock()
tb.close()

if os.path.exists(datadir+target+'.ms'): shutil.rmtree(datadir+target+'.ms')
split(vis=visname, outputvis=datadir+target+'.ms', field=targ, width=bin_width, datacolumn='corrected')

# fix state_ids to -1 to avoid errors due to missing STATE table
tb.open(datadir+target+'.ms', nomodify=False)
nrows=tb.nrows()
tb.putcol(columnname='STATE_ID', value=-1*np.ones((nrows)))
tb.unlock()
tb.close()

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

#PLOTTING
if gain1:
	if doplot:
		# plot solutions:
		plotcal(caltable=caldir+'G0-'+cal_obs, \
				xaxis='time', \
				yaxis='phase', \
				subplot=521, \
				iteration='antenna', \
				showgui=False, \
				figfile=caldir+'G0-'+cal_obs+'-phs.png', \
				plotrange=[0,0,-180,180])

if delay:
	if doplot:
		# plot solutions:
		plotcal(caltable=caldir+'K0-'+cal_obs, \
				xaxis='antenna', \
				yaxis='delay', \
				subplot=111, \
				iteration='', \
				showgui=False, \
				figfile=caldir+'K0-'+cal_obs+'.png', \
				plotrange=[])

if bndps:
	if doplot:
		# plot solutions:
		plotcal(caltable=caldir+'B0-'+cal_obs, \
				xaxis='freq', \
				yaxis='amp', \
				subplot=521, \
				iteration='antenna', \
				showgui=False, \
				figfile=caldir+'B0-'+cal_obs+'-amp.png', \
				plotrange=[])



		# plot solutions:
		plotcal(caltable=caldir+'B0-'+cal_obs, \
				xaxis='freq', \
				yaxis='phase', \
				subplot=521, \
				iteration='antenna', \
				showgui=False, \
				figfile=caldir+'B0-'+cal_obs+'-phs.png', \
				plotrange=[])

if gain2:
	if doplot:
		# plot solutions:
		plotcal(caltable=caldir+'G1-'+cal_obs, \
				field=pcal, \
				xaxis='time', \
				yaxis='amp', \
				subplot=521, \
				iteration='antenna', \
				showgui=False, \
				figfile=caldir+'G1-'+cal_obs+'-amp.png', \
				plotrange=[])


		# plot solutions:
		plotcal(caltable=caldir+'G1-'+cal_obs, \
				field=pcal, \
				xaxis='time', \
				yaxis='phase', \
				subplot=521, \
				iteration='antenna', \
				showgui=False, \
				figfile=caldir+'G1-'+cal_obs+'-phs.png', \
				plotrange=[])
if gain1:
    caltab = caldir+'G1-'+cal_obs
    if doplot:
        # plot solutions:
        plotcal(caltable=caltab, \
            field='', \
            xaxis='time', \
            yaxis='amp', \
            subplot=521, \
            iteration='antenna', \
            showgui=False, \
            figfile=caldir+'G1-'+cal_sec+'-amp.png', \
            plotrange=[])

        # plot solutions:
        plotcal(caltable=caltab, \
            field='', \
            xaxis='time', \
            yaxis='phase', \
            subplot=521, \
            iteration='antenna', \
            showgui=False, \
            figfile=caldir+'G1-'+cal_sec+'-phs.png', \
            plotrange=[0,0,-180,180])

end = timer()

print "Calibration took ",end-begin," sec"


