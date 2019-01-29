import csv
import sys

#Convert to degrees:

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



# input source list from PyBDSF:
#filename = sys.argv[1]+'.csv'
filename = target+'_LA-FLATN.csv'
# open the CSV file using universal read:
csvfile = open(filename, 'rU') 

# set up the output annotation file:
outname = target+'_LA-FLATN.ann'
outfile = open(outname,'w')

# get the FOV:
ra0 = RA2dec
dec0= Dec2dec
hwhm0= 0.20 #10./60.



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
for row in readCSV:
	ra = row[2]
	dec = row[4]
	bmaj = row[14]
	bmin = row [16]
	pa = row[18]

	bpa = float(pa)+90. 
	outfile.write('COLOR RED  \n')
	outfile.write('ELLIPSE '+ra+' '+dec+' '+bmaj+' '+bmin+' '+str(bpa)+'  \n')
outfile.write('COLOR BLUE  \n')
outfile.write('CIRCLE '+str(ra0)+' '+str(dec0)+' '+str(hwhm0)+'  \n')


outfile.close()


		
