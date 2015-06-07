# runs the contrast stimuli with larger
from sys import argv
import re
import string
import fileinput
import os
import glob
import numpy as np

import neo
from neo import io
import numpy as np
import elephant.statistics as es
import matplotlib.pylab as plt
from quantities import ms
##############################################################################################
script, conn_weight=argv
num_tc_cell = 16
num_re_cell = 12
num_in_cell = 4

def line_prepender(conn_weight, line):
    with open(conn_weight,'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write(line.rstrip('\r\n') + '\n' + content)

with open('./base/largernet.hoc') as oldver, open('./compiled/largernet_'+conn_weight+'.hoc','w') as newver: 
	for line in oldver:
		newver.write(line)        

with open('./compiled/largernet_'+conn_weight+'.hoc') as oldver, open('./largernet_'+conn_weight+'.hoc','w') as newver:
    for line in oldver:
        newver.write(line) 


with open('./base/largernet_vb_contrast.py') as oldver, open('./compiled/largernet_vb_contrast_'+conn_weight+'.py','w') as newver: 
	for line in oldver:	
		newver.write(line)        

with open('./param/'+conn_weight+'.txt') as inf: # ./param/ contains all the .txt files with different parameter settings
    for line in inf:
        line_prepender('./compiled/largernet_vb_contrast_'+conn_weight+'.py', line) # put the new file (file+parameters) into a folder called 
        															  # ./compiled, with the name of the file after the parameter
        															  # set's name, then .py as the format

with open('./compiled/largernet_vb_contrast_'+conn_weight+'.py') as oldver, open('./largernet_vb_contrast_'+conn_weight+'.py','w') as newver:
    for line in oldver:
        newver.write(line) 
##############################################################################################
###### creating directories
for ls_condition in range(1,5):
	if ls_condition == 1:
		con_number = '000'
	elif ls_condition == 2:
		con_number = '010'
	elif ls_condition == 3:
		con_number = '040'
	else:
		con_number = '100'	

	addpath='./run_lgn_pgn/largernet/'+conn_weight+'/contrast_'+con_number
	if not os.path.exists(addpath): 
		os.makedirs(addpath)

	save_relay = './run_lgn_pgn/largernet/'+conn_weight+'/contrast_'+con_number+'/relay'
	if not os.path.exists(save_relay): 
		os.makedirs(save_relay)
	for i in range (0, num_tc_cell):
		save_tc_cell = './run_lgn_pgn/largernet/'+conn_weight+'/contrast_'+con_number+'/relay/tc_cell'+str(i)
		if not os.path.exists(save_tc_cell): 
			os.makedirs(save_tc_cell)

	save_reticular = './run_lgn_pgn/largernet/'+conn_weight+'/contrast_'+con_number+'/reticular'
	if not os.path.exists(save_reticular): 
		os.makedirs(save_reticular)
	for i in range (0, num_re_cell):
		save_re_cell = './run_lgn_pgn/largernet/'+conn_weight+'/contrast_'+con_number+'/reticular/re_cell'+str(i)
		if not os.path.exists(save_re_cell): 
			os.makedirs(save_re_cell)

tc_results_dat='/Users/jiemei/Desktop/TC_model/run_lgn_pgn/largernet/'+conn_weight+'/tc_csr_results_dat/'
if not os.path.exists(tc_results_dat): 
	os.makedirs(tc_results_dat)	

re_results_dat='/Users/jiemei/Desktop/TC_model/run_lgn_pgn/largernet/'+conn_weight+'/re_csr_results_dat/'
if not os.path.exists(re_results_dat): 
	os.makedirs(re_results_dat)	

##############################################################################################
###### changing input file to largernet.hoc
######

for ls_condition in range(1,5):	
	for trial_num in range(1,101):	
		if ls_condition == 1:
			con_number = '000'
		if ls_condition == 2:
			con_number = '010'
		if ls_condition == 3:
			con_number = '040'
		if ls_condition == 4:
			con_number = '100'	

		f=open('/Users/jiemei/Desktop/TC_model/param/input_retinal.txt','w') # completing the parameter file by adding the path for accesing the .spk
		spiking15='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_4136/csr'+con_number+'_rgccell_4136_0'+str(trial_num)+'.dat"'
		spiking14='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_4080/csr'+con_number+'_rgccell_4080_0'+str(trial_num)+'.dat"'
		spiking13='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_4186/csr'+con_number+'_rgccell_4186_0'+str(trial_num)+'.dat"'
		spiking12='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_4086/csr'+con_number+'_rgccell_4086_0'+str(trial_num)+'.dat"'
		spiking11='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_4078/csr'+con_number+'_rgccell_4078_0'+str(trial_num)+'.dat"'
		spiking10='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_3978/csr'+con_number+'_rgccell_3978_0'+str(trial_num)+'.dat"'
		spiking9='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_4084/csr'+con_number+'_rgccell_4084_0'+str(trial_num)+'.dat"'
		spiking8='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_4028/csr'+con_number+'_rgccell_4028_0'+str(trial_num)+'.dat"'
		
		spiking7='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_1274/csr'+con_number+'_rgccell_1274_0'+str(trial_num)+'.dat"'
		spiking6='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_1376/csr'+con_number+'_rgccell_1376_0'+str(trial_num)+'.dat"'
		spiking5='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_1482/csr'+con_number+'_rgccell_1482_0'+str(trial_num)+'.dat"'
		spiking4='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_1374/csr'+con_number+'_rgccell_1374_0'+str(trial_num)+'.dat"'
		spiking3='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_1382/csr'+con_number+'_rgccell_1382_0'+str(trial_num)+'.dat"'
		spiking2='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_1537/csr'+con_number+'_rgccell_1537_0'+str(trial_num)+'.dat"'
		spiking1='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_1380/csr'+con_number+'_rgccell_1380_0'+str(trial_num)+'.dat"'
		spiking0='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_1276/csr'+con_number+'_rgccell_1276_0'+str(trial_num)+'.dat"'
		f.write('spiking15='+spiking15+'\n')
		f.write('spiking14='+spiking14+'\n')
		f.write('spiking13='+spiking13+'\n')
		f.write('spiking12='+spiking12+'\n')	
		f.write('spiking11='+spiking11+'\n')
		f.write('spiking10='+spiking10+'\n')
		f.write('spiking9='+spiking9+'\n')
		f.write('spiking8='+spiking8+'\n')	
		f.write('spiking7='+spiking7+'\n')
		f.write('spiking6='+spiking6+'\n')
		f.write('spiking5='+spiking5+'\n')
		f.write('spiking4='+spiking4+'\n')	
		f.write('spiking3='+spiking3+'\n')
		f.write('spiking2='+spiking2+'\n')
		f.write('spiking1='+spiking1+'\n')
		f.write('spiking0='+spiking0+'\n')	
		f.write('strdef spiking8, spiking9, spiking10, spiking11, spiking12, spiking13, spiking14, spiking15\n')
		f.write('strdef spiking0, spiking1, spiking2, spiking3, spiking4, spiking5, spiking6, spiking7\n')		
		f.close()

		with open('/Users/jiemei/Desktop/TC_model/param/input_retinal.txt') as ref1: # add parameters from the complete parameter file to the python script to run, then run it
			for lines in ref1:
				line_prepender('largernet_'+conn_weight+'.hoc', lines)

		f=open('/Users/jiemei/Desktop/TC_model/param/hoc_name.txt','w')
		new_hoc_file = 'largernet_'+conn_weight+'.hoc'
		f.write('hocfile= "'+new_hoc_file+'"'+'\n')
		dir_tc = './run_lgn_pgn/largernet/'+conn_weight+'/contrast_'+con_number+'/relay/tc_cell' # cell 0...n
		dir_re = './run_lgn_pgn/largernet/'+conn_weight+'/contrast_'+con_number+'/reticular/re_cell'
		f.write('dir_tc = "'+dir_tc+'"'+'\n')	
		f.write('dir_re = "'+dir_re+'"'+'\n')	
		f.write('condition_id = "'+con_number+'"\n')
		f.write('trial_id = '+str(trial_num)+'\n')
		f.write('n_tc_cell = '+str(num_tc_cell)+'\n')
		f.write('n_re_cell = '+str(num_re_cell)+'\n')
		f.write('n_in_cell = '+str(num_in_cell)+'\n')
		f.close()


		with open('/Users/jiemei/Desktop/TC_model/param/hoc_name.txt') as ref: # add parameters from the complete parameter file to the python script to run, then run it
			for lines in ref:
				print lines
				line_prepender('largernet_vb_contrast_'+conn_weight+'.py', lines)
		
		os.system('python '+ 'largernet_vb_contrast_'+conn_weight+'.py')

		os.remove('largernet_vb_contrast_'+conn_weight+'.py')
		os.remove('largernet_'+conn_weight+'.hoc')

		with open('./compiled/largernet_vb_contrast_'+conn_weight+'.py') as oldver, open('./largernet_vb_contrast_'+conn_weight+'.py','w') as newver:
		    for line in oldver:
		        newver.write(line) 
		with open('./compiled/largernet_'+conn_weight+'.hoc') as oldver, open('./largernet_'+conn_weight+'.hoc','w') as newver:
		    for line in oldver:
		        newver.write(line) 

# deleted the program copy in the main directory TC_model
os.chdir('/Users/jiemei/Desktop/TC_model')
os.remove('largernet_vb_contrast_'+conn_weight+'.py')		
os.remove('largernet_'+conn_weight+'.hoc')

for ls_condition in range(1,5):
	for i in range(0, num_tc_cell):
		if ls_condition == 1:
			con_number = '000'
		if ls_condition == 2:
			con_number = '010'
		if ls_condition == 3:
			con_number = '040'
		if ls_condition == 4:
			con_number = '100'	

		tc_results = '/run_lgn_pgn/largernet/'+conn_weight+'/contrast_'+con_number+'/relay/tc_cell'
		os.chdir('/Users/jiemei/Desktop/TC_model'+tc_results+str(i))

		read_files = glob.glob("*.dat")

		with open(tc_results_dat+'tc_cell'+str(i)+'_csr'+con_number+'.dat', "wb") as outfile:
		    for f in read_files:
		        with open(f, "rb") as infile:
					outfile.write(infile.read())

	#for ii in range(1, num_condition+1):
	for i in range(0, num_re_cell):	
		if ls_condition == 1:
			con_number = '000'
		if ls_condition == 2:
			con_number = '010'
		if ls_condition == 3:
			con_number = '040'
		if ls_condition == 4:
			con_number = '100'			
		
		re_results = '/run_lgn_pgn/largernet/'+conn_weight+'/contrast_'+con_number+'/reticular/re_cell'
		os.chdir('/Users/jiemei/Desktop/TC_model'+re_results+str(i))

		read_files = glob.glob("*.dat")

		with open(re_results_dat+'re_cell'+str(i)+'_csr'+con_number+'.dat', "wb") as outfile:
		    for f in read_files:
		        with open(f, "rb") as infile:
					outfile.write(infile.read())

	#for ii in range(1, num_condition+1):
	tc_plot = []
	for i in range(0, num_tc_cell):		
		if ls_condition == 1:
			con_number = '000'
		if ls_condition == 2:
			con_number = '010'
		if ls_condition == 3:
			con_number = '040'
		if ls_condition == 4:
			con_number = '100'	

		os.chdir('/Users/jiemei/Desktop/TC_model')
		tc_results = './run_lgn_pgn/largernet/'+conn_weight+'/tc_csr_results'
		if not os.path.exists(tc_results): 
			os.makedirs(tc_results)
		
		os.chdir(tc_results_dat)
		r = io.AsciiSpikeTrainIO(filename = 'tc_cell'+str(i)+'_csr'+con_number+'.dat')
		seg = r.read_segment(unit=ms)
		#print seg.spiketrains
		for st in seg.spiketrains:
			st.t_stop = 2400*ms
		tc_plot = es.time_histogram(seg.spiketrains, 10*ms, output='counts')    
		plt.plot(tc_plot)
		plt.ylim(0, 100)
		os.chdir('/Users/jiemei/Desktop/TC_model/run_lgn_pgn/largernet/'+conn_weight+'/tc_csr_results')
		plt.savefig('tc_cell'+str(i)+'_csr'+con_number+'.png')
		plt.close()

	re_plot = []
	for i in range(0, num_re_cell):			
		os.chdir('/Users/jiemei/Desktop/TC_model')
		re_results = './run_lgn_pgn/largernet/'+conn_weight+'/re_csr_results'
		if not os.path.exists(re_results): 
			os.makedirs(re_results)
		
		os.chdir(re_results_dat)		
		r = io.AsciiSpikeTrainIO(filename = 're_cell'+str(i)+'_csr'+con_number+'.dat')
		seg = r.read_segment(unit=ms)
		#print seg.spiketrains
		for st in seg.spiketrains:
			st.t_stop = 2400*ms
		re_plot = es.time_histogram(seg.spiketrains, 10*ms, output='counts')    
		plt.plot(re_plot)
		plt.ylim(0, 100)
		os.chdir('/Users/jiemei/Desktop/TC_model/run_lgn_pgn/largernet/'+conn_weight+'/re_csr_results')
		plt.savefig('re_cell'+str(i)+'_csr'+con_number+'.png')
		plt.close()
