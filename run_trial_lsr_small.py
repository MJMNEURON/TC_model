##############################################################################################
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
num_tc_cell = 4
num_re_cell = 2

def line_prepender(conn_weight, line):
    with open(conn_weight,'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write(line.rstrip('\r\n') + '\n' + content)

with open('./base/smallnet.hoc') as oldver, open('./compiled/smallnet_'+conn_weight+'.hoc','w') as newver: 
	for line in oldver:
		newver.write(line)        

with open('./compiled/smallnet_'+conn_weight+'.hoc') as oldver, open('./smallnet_'+conn_weight+'.hoc','w') as newver:
    for line in oldver:
        newver.write(line) 

with open('./base/smallnet_vb_lsr.py') as oldver, open('./compiled/smallnet_vb_lsr_'+conn_weight+'.py','w') as newver: 
	for line in oldver:	
		newver.write(line)        

with open('./param/'+conn_weight+'.txt') as inf: # ./param/ contains all the .txt files with different parameter settings
    for line in inf:
        line_prepender('./compiled/smallnet_vb_lsr_'+conn_weight+'.py', line) # put the new file (file+parameters) into a folder called 
        															  # ./compiled, with the name of the file after the parameter
        															  # set's name, then .py as the format

with open('./compiled/smallnet_vb_lsr_'+conn_weight+'.py') as oldver, open('./smallnet_vb_lsr_'+conn_weight+'.py','w') as newver:
    for line in oldver:
        newver.write(line) 
##############################################################################################
###### creating directories
for iii in range(3,7):  # two light spot conditions
	addpath='./run_lgn_pgn/smallnet/'+conn_weight+'/light_spot_'+str(iii)
	if not os.path.exists(addpath): 
		os.makedirs(addpath)
	
	save_relay = './run_lgn_pgn/smallnet/'+conn_weight+'/light_spot_'+str(iii)+'/relay'
	if not os.path.exists(save_relay): 
		os.makedirs(save_relay)
	for i in range (0, num_tc_cell):
		save_tc_cell = './run_lgn_pgn/smallnet/'+conn_weight+'/light_spot_'+str(iii)+'/relay/tc_cell'+str(i)
		if not os.path.exists(save_tc_cell): 
			os.makedirs(save_tc_cell)
	
	save_reticular = './run_lgn_pgn/smallnet/'+conn_weight+'/light_spot_'+str(iii)+'/reticular'
	if not os.path.exists(save_reticular): 
		os.makedirs(save_reticular)
	for i in range (0, num_re_cell):
		save_re_cell = './run_lgn_pgn/smallnet/'+conn_weight+'/light_spot_'+str(iii)+'/reticular/re_cell'+str(i)
		if not os.path.exists(save_re_cell): 
			os.makedirs(save_re_cell)

tc_results_dat='/Users/jiemei/Desktop/TC_model/run_lgn_pgn/smallnet/'+conn_weight+'/tc_lsr_results_dat/'
if not os.path.exists(tc_results_dat): 
	os.makedirs(tc_results_dat)	

re_results_dat='/Users/jiemei/Desktop/TC_model/run_lgn_pgn/smallnet/'+conn_weight+'/re_lsr_results_dat/'
if not os.path.exists(re_results_dat): 
	os.makedirs(re_results_dat)

##############################################################################################
###### changing input file to smallnet.hoc
######
for ls_condition in range(3,7):
	for trial_num in range(1,101):		
		f=open('/Users/jiemei/Desktop/TC_model/param/input_retinal.txt','w') # completing the parameter file by adding the path for accesing the .spk
		spiking3='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4084/lsr0'+str(ls_condition)+'_rgccell_4084'+'_0'+str(trial_num)+'.dat"'
		spiking2='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4080/lsr0'+str(ls_condition)+'_rgccell_4080'+'_0'+str(trial_num)+'.dat"'
		spiking1='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1380/lsr0'+str(ls_condition)+'_rgccell_1380'+'_0'+str(trial_num)+'.dat"'
		spiking0='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1376/lsr0'+str(ls_condition)+'_rgccell_1376'+'_0'+str(trial_num)+'.dat"'
		f.write('spiking3='+spiking3+'\n')
		f.write('spiking2='+spiking2+'\n')
		f.write('spiking1='+spiking1+'\n')
		f.write('spiking0='+spiking0+'\n')	
		f.write('strdef spiking0, spiking1, spiking2, spiking3\n')
		f.close()

		with open('/Users/jiemei/Desktop/TC_model/param/input_retinal.txt') as ref1: # add parameters from the complete parameter file to the python script to run, then run it
			for lines in ref1:
				line_prepender('smallnet_'+conn_weight+'.hoc', lines)
	
		f=open('/Users/jiemei/Desktop/TC_model/param/hoc_name.txt','w')
		new_hoc_file = 'smallnet_'+conn_weight+'.hoc'
		f.write('hocfile= "'+new_hoc_file+'"'+'\n')
		dir_tc = './run_lgn_pgn/smallnet/'+conn_weight+'/light_spot_'+str(ls_condition)+'/relay/tc_cell' # cell 0...n
		dir_re = './run_lgn_pgn/smallnet/'+conn_weight+'/light_spot_'+str(ls_condition)+'/reticular/re_cell'
		f.write('dir_tc = "'+dir_tc+'"'+'\n')	
		f.write('dir_re = "'+dir_re+'"'+'\n')	
		f.write('condition_id = '+str(ls_condition)+'\n')
		f.write('trial_id = '+str(trial_num)+'\n')
		f.write('n_tc_cell = '+str(num_tc_cell)+'\n')
		f.write('n_re_cell = '+str(num_re_cell)+'\n')
		f.close()

		with open('/Users/jiemei/Desktop/TC_model/param/hoc_name.txt') as ref: # add parameters from the complete parameter file to the python script to run, then run it
			for lines in ref:
				print lines
				line_prepender('smallnet_vb_lsr_'+conn_weight+'.py', lines)
		
		os.system('python '+ 'smallnet_vb_lsr_'+conn_weight+'.py')

		os.remove('smallnet_vb_lsr_'+conn_weight+'.py')
		os.remove('smallnet_'+conn_weight+'.hoc')

		with open('./compiled/smallnet_vb_lsr_'+conn_weight+'.py') as oldver, open('./smallnet_vb_lsr_'+conn_weight+'.py','w') as newver:
		    for line in oldver:
		        newver.write(line) 
		with open('./compiled/smallnet_'+conn_weight+'.hoc') as oldver, open('./smallnet_'+conn_weight+'.hoc','w') as newver:
		    for line in oldver:
		        newver.write(line) 

# deleted the program copy in the main directory TC_model
os.chdir('/Users/jiemei/Desktop/TC_model')
os.remove('smallnet_vb_lsr_'+conn_weight+'.py')		
os.remove('smallnet_'+conn_weight+'.hoc')

#num_condition=6 # CHANGE THIS!
for ii in range(3,7):
	for i in range(0, num_tc_cell):
		tc_results = '/run_lgn_pgn/smallnet/'+conn_weight+'/light_spot_'+str(ii)+'/relay/tc_cell'
		os.chdir('/Users/jiemei/Desktop/TC_model'+tc_results+str(i))

		read_files = glob.glob("*.dat")
		
		with open(tc_results_dat+'tc_cell'+str(i)+'_lsr0'+str(ii)+'.dat', "wb") as outfile:
		    for f in read_files:
		        with open(f, "rb") as infile:
					outfile.write(infile.read())

for ii in range(3,7):
	for i in range(0, num_re_cell):
		re_results = '/run_lgn_pgn/smallnet/'+conn_weight+'/light_spot_'+str(ii)+'/reticular/re_cell'
		os.chdir('/Users/jiemei/Desktop/TC_model'+re_results+str(i))

		read_files = glob.glob("*.dat")
		
		with open(re_results_dat+'re_cell'+str(i)+'_lsr0'+str(ii)+'.dat', "wb") as outfile:
		    for f in read_files:
		        with open(f, "rb") as infile:
					outfile.write(infile.read())

for ii in range(3,7):
	tc_plot = []
	for i in range(0, num_tc_cell):
		os.chdir('/Users/jiemei/Desktop/TC_model')
		tc_results = './run_lgn_pgn/smallnet/'+conn_weight+'/tc_lsr_results'
		if not os.path.exists(tc_results): 
			os.makedirs(tc_results)

		os.chdir(tc_results_dat)
		r = io.AsciiSpikeTrainIO(filename = 'tc_cell'+str(i)+'_lsr0'+str(ii)+'.dat')
		seg = r.read_segment(unit=ms)
		#print seg.spiketrains
		for st in seg.spiketrains:
			st.t_stop = 2400*ms
		tc_plot = es.time_histogram(seg.spiketrains, 2*ms, output='counts')    
		plt.plot(tc_plot)

		os.chdir('/Users/jiemei/Desktop/TC_model/run_lgn_pgn/smallnet/'+conn_weight+'/tc_lsr_results')
		plt.savefig('tc_cell'+str(i)+'_lsr0'+str(ii)+'.png')
		plt.close()

for ii in range(3,7):
	re_plot = []
	for i in range(0, num_re_cell):
		os.chdir('/Users/jiemei/Desktop/TC_model')
		re_results = './run_lgn_pgn/smallnet/'+conn_weight+'/re_lsr_results'
		if not os.path.exists(re_results): 
			os.makedirs(re_results)
		
		os.chdir(re_results_dat)
		r = io.AsciiSpikeTrainIO(filename = 're_cell'+str(i)+'_lsr0'+str(ii)+'.dat')
		seg = r.read_segment(unit=ms)
		#print seg.spiketrains
		for st in seg.spiketrains:
			st.t_stop = 2400*ms
		re_plot = es.time_histogram(seg.spiketrains, 2*ms, output='counts')    
		plt.plot(re_plot)
		plt.ylim(0, 60)
		os.chdir('/Users/jiemei/Desktop/TC_model/run_lgn_pgn/smallnet/'+conn_weight+'/re_lsr_results')
		plt.savefig('re_cell'+str(i)+'_lsr0'+str(ii)+'.png')
		plt.close()
