import numpy as np
import csv

RAdec = dict()
Decdec = dict()
RArad = dict()
Decrad = dict()
InitialFlux = dict()
RAdif = dict()
Decdif = dict()
RAdifAM = dict()
DecdifAM = dict()
DistAM = dict()
X = dict()
fluxratio = dict()
flux = dict()
coords = dict()

RASH = 11	#Change this to you cluster Right Ascension in hours
RASM = 34	#Change this to you cluster Right Ascension in minutes
RASS = 50.5	#Change this to you cluster Right Ascension in seconds
DECSD = 49	#Change this to you cluster declination in degrees
DECSM = 03	#Change this to you cluster declination in minutes
DECSS = 28	#Change this to you cluster declination in seconds

PBPARM3 = -0.0287276
PBPARM4 = 0.00358632
PBPARM5 = -0.0000182809

with open('A1314-LAPB-160517.csv') as csvfile: #Change this to your csv from pybdsm- Delete the titles at the top of the csv!!!! (Source_id, Isl_id, ... etc.)
	readCSV = csv.reader(csvfile, delimiter=',')
	Source_ids = []
	Isl_ids = []
	RAs = []
	E_RAs = [] 
	Decs = []
	E_DECs = []
	Total_fluxs = []
	E_Total_fluxs = []
	Peak_fluxs = []
	E_Peak_fluxs = []
	RA_maxs = []
	E_RA_maxs = [] 
	DEC_maxs = []
	E_DEC_maxs = []
	Majs = []
	E_Majs = []
	Mins = []
	E_Mins = []
	PAs = []
	E_PAs = []
	Maj_img_planes = []
	E_Maj_img_planes = []
	Min_img_planes = []
	E_Min_img_planes = []
	PA_img_planes = []
	E_PA_img_planes = []
	DC_Majs = []
	E_DC_Majs = [] 
	DC_Mins = []
	E_DC_Mins = []
	DC_PAs = []
	E_DC_PAs = []	
	DC_Maj_img_planes = []
	E_DC_Maj_img_planes = [] 
	DC_Min_img_planes = [] 
	E_DC_Min_img_planes = []
	DC_PA_img_planes = [] 
	E_DC_PA_img_planes = [] 
	Isl_Total_fluxs = []
	E_Isl_Total_fluxs = []
	Isl_rmss = []
	Isl_means = []
	Resid_Isl_rmss = []
	Resid_Isl_means = []
	S_Codes = []
	for row in readCSV:
		Source_id = row[0]
		Isl_id = row[1]
		RA = row[2]
		E_RA = row[3] 
		Dec = row[4]
		E_DEC= row[5]
		Total_flux = row[6]
		E_Total_flux = row[7]
		Peak_flux = row[8]
		E_Peak_flux = row[9]
		RA_max = row[10]
		E_RA_max = row[11] 
		DEC_max = row[12]
		E_DEC_max = row[13]
		Maj = row[14]
		E_Maj = row[15]
		Min = row [16]
		E_Min = row[17]
		PA = row[18]
		E_PA = row[19]
		Maj_img_plane = row[20]
		E_Maj_img_plane = row[21]
		Min_img_plane = row[22]
		E_Min_img_plane = row[23]
		PA_img_plane = row[24]
		E_PA_img_plane = row[25]
		DC_Maj = row[26]
		E_DC_Maj = row[27] 
		DC_Min = row[28]
		E_DC_Min = row[29]
		DC_PA = row[30]
		E_DC_PA = row[31]
		DC_Maj_img_plane = row[32]
		E_DC_Maj_img_plane = row[33] 
		DC_Min_img_plane = row[34] 
		E_DC_Min_img_plane = row[35]
		DC_PA_img_plane = row[36]
		E_DC_PA_img_plane = row[37]
		Isl_Total_flux = row[38]
		E_Isl_Total_flux = row[39]
		Isl_rms = row[40]
		Isl_mean = row[41]
		Resid_Isl_rms = row[42]
		Resid_Isl_mean = row[43]
		S_Code = row[44]

		Source_ids.append(float(Source_id))
		Isl_ids.append(float(Isl_id))
		RAs.append(float(RA))
		E_RAs.append(float(E_RA))
		Decs.append(float(Dec))
		E_DECs.append(float(E_DEC))
		Total_fluxs.append(float(Total_flux))
		E_Total_fluxs.append(float(E_Total_flux))
		Peak_fluxs.append(float(Peak_flux))
		E_Peak_fluxs.append(float(E_Peak_flux))
		RA_maxs.append(float(RA_max))
		E_RA_maxs.append(float(E_RA_max))
		DEC_maxs.append(float(DEC_max))
		E_DEC_maxs.append(float(E_DEC_max))
		Majs.append(float(Maj))
		E_Majs.append(float(E_Maj))
		Mins.append(float(Min))
		E_Mins.append(float(E_Min))
		PAs.append(float(PA))
		E_PAs.append(float(E_PA))
		Maj_img_planes.append(float(Maj_img_plane))
		E_Maj_img_planes.append(float(E_Maj_img_plane))
		Min_img_planes.append(float(Min_img_plane))
		E_Min_img_planes.append(float(E_Min_img_plane))
		PA_img_planes.append(float(PA_img_plane))
		E_PA_img_planes.append(float(E_PA_img_plane))
		DC_Majs.append(float(DC_Maj))
		E_DC_Majs.append(float(E_DC_Maj))
		DC_Mins.append(float(DC_Min))
		E_DC_Mins.append(float(E_DC_Min))
		DC_PAs.append(float(DC_PA))
		E_DC_PAs.append(float(E_DC_PA))
		DC_Maj_img_planes.append(float(DC_Maj_img_plane))
		E_DC_Maj_img_planes.append(float(E_DC_Maj_img_plane))
		DC_Min_img_planes.append(float(DC_Min_img_plane))
		E_DC_Min_img_planes.append(float(E_DC_Min_img_plane))
		DC_PA_img_planes.append(float(DC_PA_img_plane)) 
		E_DC_PA_img_planes.append(float(E_DC_PA_img_plane)) 
		Isl_Total_fluxs.append(float(Isl_Total_flux))
		E_Isl_Total_fluxs.append(float(E_Isl_Total_flux))
		Isl_rmss.append(float(Isl_rms))
		Isl_means.append(float(Isl_mean))
		Resid_Isl_rmss.append(float(Resid_Isl_rms))
		Resid_Isl_means.append(float(Resid_Isl_mean))
		S_Codes.append(S_Code)

RASdec = (RASH * 15.00000000000000000) + (RASM/4.000000000000000000000) + (RASS/240.00000000000000000)
DecSdec= (DECSD) + (DECSM/60.00000000000000000) + (DECSS/3600.0000000000000000)



for i in range(0,35):  		#Change this to your maximum source_id plus one

	RAdif[i] = abs(RAs[i] - RASdec)
	Decdif[i] = abs(Decs[i] - DecSdec)

	RAdifAM[i] = RAdif[i] *60 * cos(Decs[i]*(pi/180))
	DecdifAM[i] = Decdif[i] *60

	DistAM[i] = ((RAdifAM[i]**2.00000000000)+(DecdifAM[i]**2.000000000000))**0.5

	X[i] = (DistAM[i] *15)** 2.0000000000000

	fluxratio[i] = 1 +((X[i]*PBPARM3)/(10**3.00000000))+((X[i]*X[i]*PBPARM4)/(10**7.0000000))+((X[i]*X[i]*X[i]*PBPARM5)/(10**10.000000))

	flux[i] = Total_fluxs[i] * fluxratio[i]


	cl.addcomponent(flux=flux[i], fluxunit='Jy', shape='point', dir="J2000 "+ str(RAs[i])+'deg '+str(Decs[i])+'deg' ) #Adjust this using the same idea if needs changing between point source and gaussian.

for n in reversed(xrange(35)):  #Change this to your maximum source_id plus one
	if flux[n] < -0.0:	#May want to change this if need more sources to be removed from component list and then not subtracted
		cl.remove([n])

cl.rename('A1314-LAPB-160517.cl')	#Change this to whatever you want to call your component list
cl.done
