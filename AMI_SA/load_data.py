from timeit import default_timer as timer

begin = timer()

execfile('/home/fdantas/mytasks/mytasks.py')

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

target_idi  = '/scratch/nas_toothless/Clarke_Clusters/SA/A399-160912.idi'
pcal_idi = '/scratch/nas_toothless/Calibrators/SA/3C286-160912.idi'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

cal_obs = '3C286'
cal_sec = 'J0309+1029'
target = 'A399'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

datadir = '../DATA/'
#caldir = '../CALIBRATION/'
caldir = datadir

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

origvis = datadir+target+'_wc.MS'   # 'wc'  = 'with calibrator'
visname = datadir+target+'_fxd.MS'  # 'fxd' = 'scan numbers fixed'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

if not os.path.exists(origvis):
	print "Importing the data from FITSIDI --> MS: importfitsidi()"
	os.system('rm -rf temp.*  \n')
	importfitsidi(fitsidifile=[pcal_idi], vis=datadir+'temp1.ms')
	if not os.path.exists(cal_obs+'.rain'):
		try:
			mytsys=[]
			gencal_rain(vis=datadir+'temp1.ms', fitsidifile=pcal_idi, \
					caltable=caldir+cal_obs+'.rain', continuum=True, tsys=mytsys)
			
			print "Making raingauge table for calibrator  --> "+cal_obs+".rain: gencal_rain()"
			plotcal(caltable=caldir+cal_obs+'.rain', xaxis='time', yaxis='amp', \
					figfile=caldir+cal_obs+'_rain.png', showgui=False)
		
	  	except:
			# No rain gauge table attached to FITS file, rain gauge correction already applied
			print "This must be a pre-[161101] observation"
			print "Raingauge applied to FITSIDI directly"
			pass

	importfitsidi(fitsidifile=[target_idi], vis=datadir+'temp2.ms')
	if not os.path.exists(target+'.rain'):
		try:
			mytsys=[]
			gencal_rain(vis=datadir+'temp2.ms', fitsidifile=target_idi,\
					 caltable=caldir+target+'.rain', continuum=True, tsys=mytsys)
			
			print "Making raingauge table for target  --> "+target+".rain: gencal_rain()"
			plotcal(caltable=caldir+cal_obs+'.rain', xaxis='time', yaxis='amp', \
					figfile=caldir+cal_obs+'_rain.png', showgui=False)
		except:
			# No rain gauge table attached to FITS file, rain gauge correction already applied
			print "This must be a pre-[161101] observation"
			print "Raingauge applied to FITSIDI directly"
			pass

	concat(vis=[datadir+'temp1.ms',datadir+'temp2.ms'],concatvis = origvis)
	os.system('rm -rf temp* \n')
	print ">>> Created: "+origvis


# ---
# Fix scan numbers in MS:
if not os.path.exists(visname):
	print "Fixing the scan numbers: fixscan()"
	fixscan(vis=origvis,outputvis=visname)
	print ">>> Created: "+visname


end = timer()

print "Loading took ",end-begin," sec"


