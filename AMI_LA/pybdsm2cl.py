import csv
import sys
import numpy as np

target = 'A399' #02,57,50.000, +13,03,16.461

#Convert to degrees:



RASH = 2.000	#Change this to you cluster Right Ascension in hours
RASM = 57.000	#Change this to you cluster Right Ascension in minutes
RASS = 50.000	#Change this to you cluster Right Ascension in seconds
DECSD = 13.000	#Change this to you cluster declination in degrees
DECSM = 3.000	#Change this to you cluster declination in minutes
DECSS = 16.461	#Change this to you cluster declination in seconds


RA2dec = (RASH * 15.000) + (RASM/4.000) + (RASS/240.000)
Dec2dec= (DECSD) + (DECSM/60.000) + (DECSS/3.6e3)

print RA2dec
print Dec2dec


# AMI-SA primary beam parameters:
PBPARM3 = -0.0287276
PBPARM4 = 0.00358632
PBPARM5 = -0.0000182809

# input source list from PyBDSF:
filename = target+'_LA-FLATN.csv'

# open the CSV file using universal read:
csvfile = open(filename, 'rU') 

# set up the output annotation file:
outname = target+'_LA-FLATN.cl'

# get the FOV:
ra0 = RA2dec
dec0= Dec2dec

# set up a CSV reader:
readCSV = csv.reader(csvfile, delimiter=',')
	
# skip the header:
next(csvfile, None)
next(csvfile, None)
next(csvfile, None)
next(csvfile, None)

# skip the column headings:
next(csvfile, None)
next(csvfile, None)

# read the source data:
ra=[];dec=[];flux=[]
for row in readCSV:
	ra.append(float(row[2]))
	dec.append(float(row[4]))
	flux.append(float(row[6]))


for i in range(0,len(ra)):  		

	# calculate delta RA relative to field centre [deg]:
	delta_ra = abs(ra[i] - ra0)*np.cos(dec0*np.pi/180.)

	# calculate delta dec relative to field centre [deg]:
	delta_dec = abs(dec[i] - dec0)

	# calculate radial distance from field centre [deg]:
	dist_r = np.sqrt(delta_ra**2 + delta_dec**2)
	
	# calculate the AIPS X quantity (r[arcmin]*freq[GHz])^2:
	X = (dist_r*60.*15.)**2

	# calculate primary beam attenuation at that distance:
	att = 1 +((X*PBPARM3)/(1e3))+((X**2*PBPARM4)/(1e7))+((X**3*PBPARM5)/(1e10))

	# attenuate flux density appropriately:
	att_flux = att*flux[i]
	
	print "Flux check:-------->",flux[i]
	print "Att_Flux check:---->", att_flux

	# add 
	if (flux[i]>0.) and (dist_r<0.200):

		cl.addcomponent(flux=att_flux, fluxunit='Jy', shape='point',\
					dir="J2000 "+ str(ra[i])+'deg '+str(dec[i])+'deg' ) 


cl.rename(outname)	
cl.done

