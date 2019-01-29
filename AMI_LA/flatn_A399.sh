#!/bin/sh 



msfits='PWD:A399-UV.FITS' 
myname='A399_LA'  
outname='PWD:A399_LA-FLATN.fits'  
phasecnt='02,57,50.000, +13,03,16.461'  
nfield=61  
imsize1=256  
imsize2=512  
cell=4.5  

# =========================================================================================

imname=$myname
pbname=$myname 
niter=500
nchav=8
myparm='0,1,-0.3539,0.5443,-0.3418' # Set the PB parameters

aips notv << eof

5041

recat
for i=1 to 300;getn i;zap;wait;end

clrmsg


default 'fitld'
datain '$msfits'
outname '$myname'
inp
go fitld
waittask fitld


default 'indxr'
inname '$myname'
inclass 'UVDATA'
inp
go indxr
waittask indxr


default 'split'
inname '$myname'
inclass 'UVDATA'
go split
waittask split

getn 1;zap
recat

default 'imagr'
getn 1
outname '$imname'
cellsize $cell
imsize $imsize1
niter $niter
nchav $nchav
uvwtfn 'N'
go imagr
waittask imagr

for i=2 to $nfield;tget imagr;getn i;go imagr;waittask imagr;end



default 'flatn'
getn 64
outname '$pbname'
nmaps 120
imsize $imsize2
coordina $phasecnt
pbparm $myparm
inp



go flatn
waittask flatn


default 'fittp'
getn 62
dataout '$outname'
go fittp
waittask fittp


uc
kleenex

eof
