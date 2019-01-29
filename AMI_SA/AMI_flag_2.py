import numpy as np
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

datadir = '../DATA/'
caldir = '../CALIBRATION/'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

cal_obs = '3C286'
cal_sec = 'J0309+1029'
target = 'A399'

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

for i in range(4,6):
	try:
		imagename = datadir+target+'_im.image'
		rfi_box = 'rfi_box_'+str(i)+'.crtf'
		rfi_image=datadir+'rfi_box_'+str(i)+'.image'
		activems= datadir+target+'.ms'
		FIELD=target

		print 'Making model image of rfi ...'
		ia.open(imagename)
		myRGN = rg.fromtextfile(filename=rfi_box, shape=ia.shape(), csys=ia.coordsys().torecord())
		ia.subimage(outfile=rfi_image, region=myRGN, overwrite=true)
		ia.close()

		print 'FT rfi model...'
		ft(vis=activems,field=FIELD,spw="",model=rfi_image,nterms=1,reffreq="",complist="",incremental=False,usescratch=True)

		#print 'Saving old flagging...'
		flagmanager(vis=activems,mode="save",versionname="BeforeAMIAutoFlag",oldname="",comment="",merge="replace")


		print 'Starting Automated Flagging'

		msmd.open(activems)
		scan_num=msmd.scansforfield(FIELD)
		msmd.close()

		ms.open(activems)  
		for x in scan_num: 
			BadBase=[]
			ms.select({'scan_number':[x]})
			print 'Flagging Scan: '+str(x)
			ms.selectchannel(32,0,1,1)
			amp=ms.getdata(['model_amplitude'])
			amp=amp['model_amplitude']
			average = np.mean(amp[np.nonzero(amp)])
			sig = 3*average
			print 'The average amplitude is '+str(average)+' and 3sigma is '+str(sig)
			ms.selectinit(True)
			for a1 in range(0,10):
				for a2 in range(0,10):
					if a1!=a2 and a1<a2:
						ms.selectchannel(32,0,1,1)
						ms.select({'antenna1':[a1],'antenna2':[a2],'scan_number':[x]})
						base_amp=ms.getdata(['model_amplitude'])
						base_amp=base_amp['model_amplitude']
						base_average = np.mean(base_amp[np.nonzero(base_amp)])
						print 'Baseline Average for '+str(a1)+'&'+str(a2)+' is '+str(base_average)
						if base_average/average > 3.0:
							NewBadBase=str(a1)+'&'+str(a2)
							BadBase.append(NewBadBase)
						ms.selectinit(True)
			if not BadBase:
				print 'No Bad Baselines in scan '+str(x)
				casalog.post('No Bad Baselines in scan ' +str(x))
			else:
				BadBase=';'.join(BadBase)
				print 'SCAN: '+str(x)+' Bad Baselines: '+ BadBase
				casalog.post('SCAN: '+str(x)+' Bad Baselines: '+ BadBase)
					
					
		
				SCAN=str(x)
				flagdata(vis=activems,mode='manual',field=FIELD,spw='',antenna=BadBase,scan=SCAN,action='apply',display='none',flagbackup=False)

		ms.close()
	except ValueError:
		print "error"
		continue


