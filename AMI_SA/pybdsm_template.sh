
# =========================================================================================

pybdsm << eof

inp process_image

filename = '$infile'

advanced_opts = True

output_opts = True 

rms_map = True  

savefits_rmsim = True

rms_box = (60,15)

thresh = 'hard'

thresh_isl = 3.0

thresh_pix = 5.0

inp write_catalog

outfile = '$outfile'

format = 'csv'

eof
