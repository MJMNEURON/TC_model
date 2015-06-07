# # runs the light spot stimuli with largernet
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
#filenameext= # conn_weight_01.txt, conn_weight_02.txt...
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


with open('./base/largernet_vb_lsr.py') as oldver, open('./compiled/largernet_vb_lsr_'+conn_weight+'.py','w') as newver: 
	for line in oldver:	
		newver.write(line)        

with open('./param/'+conn_weight+'.txt') as inf: # ./param/ contains all the .txt files with different parameter settings
    for line in inf:
        line_prepender('./compiled/largernet_vb_lsr_'+conn_weight+'.py', line) # put the new file (file+parameters) into a folder called 
        															  # ./compiled, with the name of the file after the parameter
        															  # set's name, then .py as the format

with open('./compiled/largernet_vb_lsr_'+conn_weight+'.py') as oldver, open('./largernet_vb_lsr_'+conn_weight+'.py','w') as newver:
    for line in oldver:
        newver.write(line) 
##############################################################################################
###### creating directories
for iii in range (3,7):  # two light spot conditions
	addpath='./run_lgn_pgn/largernet/'+conn_weight+'/light_spot_'+str(iii)
	if not os.path.exists(addpath): 
		os.makedirs(addpath)
	
	save_relay = './run_lgn_pgn/largernet/'+conn_weight+'/light_spot_'+str(iii)+'/relay'
	if not os.path.exists(save_relay): 
		os.makedirs(save_relay)
	for i in range (0, num_tc_cell):
		save_tc_cell = './run_lgn_pgn/largernet/'+conn_weight+'/light_spot_'+str(iii)+'/relay/tc_cell'+str(i)
		if not os.path.exists(save_tc_cell): 
			os.makedirs(save_tc_cell)
	
	save_reticular = './run_lgn_pgn/largernet/'+conn_weight+'/light_spot_'+str(iii)+'/reticular'
	if not os.path.exists(save_reticular): 
		os.makedirs(save_reticular)
	for i in range (0, num_re_cell):
		save_re_cell = './run_lgn_pgn/largernet/'+conn_weight+'/light_spot_'+str(iii)+'/reticular/re_cell'+str(i)
		if not os.path.exists(save_re_cell): 
			os.makedirs(save_re_cell)

tc_results_dat='/Users/jiemei/Desktop/TC_model/run_lgn_pgn/largernet/'+conn_weight+'/tc_lsr_results_dat/'
if not os.path.exists(tc_results_dat): 
	os.makedirs(tc_results_dat)	

re_results_dat='/Users/jiemei/Desktop/TC_model/run_lgn_pgn/largernet/'+conn_weight+'/re_lsr_results_dat/'
if not os.path.exists(re_results_dat): 
	os.makedirs(re_results_dat)			
##############################################################################################
###### changing input file to largernet.hoc
######
for ls_condition in range(3,7):
	for trial_num in range(1,101):	
		f=open('/Users/jiemei/Desktop/TC_model/param/input_retinal.txt','w') # completing the parameter file by adding the path for accesing the .spk
		spiking15='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4136/lsr0'+str(ls_condition)+'_rgccell_4136'+'_0'+str(trial_num)+'.dat"'
		spiking14='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4080/lsr0'+str(ls_condition)+'_rgccell_4080'+'_0'+str(trial_num)+'.dat"'
		#spiking13='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_3976/lsr0'+str(ls_condition)+'_rgccell_3976'+'_0'+str(trial_num)+'.dat"'
		spiking13='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4186/lsr0'+str(ls_condition)+'_rgccell_4186'+'_0'+str(trial_num)+'.dat"'
		
		#spiking12='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4083/lsr0'+str(ls_condition)+'_rgccell_4083'+'_0'+str(trial_num)+'.dat"'
		#spiking11='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4081/lsr0'+str(ls_condition)+'_rgccell_4081'+'_0'+str(trial_num)+'.dat"'
		spiking12='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4086/lsr0'+str(ls_condition)+'_rgccell_4086'+'_0'+str(trial_num)+'.dat"'
		spiking11='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4078/lsr0'+str(ls_condition)+'_rgccell_4078'+'_0'+str(trial_num)+'.dat"'		
		spiking10='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_3978/lsr0'+str(ls_condition)+'_rgccell_3978'+'_0'+str(trial_num)+'.dat"'
		spiking9='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4084/lsr0'+str(ls_condition)+'_rgccell_4084'+'_0'+str(trial_num)+'.dat"'
		spiking8='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_4028/lsr0'+str(ls_condition)+'_rgccell_4028'+'_0'+str(trial_num)+'.dat"'
		
		spiking7='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1274/lsr0'+str(ls_condition)+'_rgccell_1274'+'_0'+str(trial_num)+'.dat"'
		spiking6='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1376/lsr0'+str(ls_condition)+'_rgccell_1376'+'_0'+str(trial_num)+'.dat"'
		spiking5='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1482/lsr0'+str(ls_condition)+'_rgccell_1482'+'_0'+str(trial_num)+'.dat"'
		#spiking4='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1378/lsr0'+str(ls_condition)+'_rgccell_1378'+'_0'+str(trial_num)+'.dat"'
		#spiking3='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1377/lsr0'+str(ls_condition)+'_rgccell_1377'+'_0'+str(trial_num)+'.dat"'
		spiking4='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1374/lsr0'+str(ls_condition)+'_rgccell_1374'+'_0'+str(trial_num)+'.dat"'
		spiking3='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1382/lsr0'+str(ls_condition)+'_rgccell_1382'+'_0'+str(trial_num)+'.dat"'
		spiking2='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1537/lsr0'+str(ls_condition)+'_rgccell_1537'+'_0'+str(trial_num)+'.dat"'
		spiking1='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1380/lsr0'+str(ls_condition)+'_rgccell_1380'+'_0'+str(trial_num)+'.dat"'
		spiking0='"lightspot/lsr0'+str(ls_condition)+'/lsr0'+str(ls_condition)+'_rgccell_1276/lsr0'+str(ls_condition)+'_rgccell_1276'+'_0'+str(trial_num)+'.dat"'
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

		with open('/Users/jiemei/Desktop/TC_model/param/input_retinal.txt') as ref1:
			for lines in ref1:
				line_prepender('largernet_'+conn_weight+'.hoc', lines)

		f=open('/Users/jiemei/Desktop/TC_model/param/hoc_name.txt','w')
		new_hoc_file = 'largernet_'+conn_weight+'.hoc'
		f.write('hocfile= "'+new_hoc_file+'"'+'\n')
		dir_tc = './run_lgn_pgn/largernet/'+conn_weight+'/light_spot_'+str(ls_condition)+'/relay/tc_cell' # cell 0...n
		dir_re = './run_lgn_pgn/largernet/'+conn_weight+'/light_spot_'+str(ls_condition)+'/reticular/re_cell'
		f.write('dir_tc = "'+dir_tc+'"'+'\n')	
		f.write('dir_re = "'+dir_re+'"'+'\n')	
		f.write('condition_id = '+str(ls_condition)+'\n')
		f.write('trial_id = '+str(trial_num)+'\n')
		f.write('n_tc_cell = '+str(num_tc_cell)+'\n')
		f.write('n_re_cell = '+str(num_re_cell)+'\n')
		f.write('n_in_cell = '+str(num_in_cell)+'\n')
		f.close()


		with open('/Users/jiemei/Desktop/TC_model/param/hoc_name.txt') as ref: # add parameters from the complete parameter file to the python script to run, then run it
			for lines in ref:
				print lines
				line_prepender('largernet_vb_lsr_'+conn_weight+'.py', lines)
		
		os.system('python '+ 'largernet_vb_lsr_'+conn_weight+'.py')

		os.remove('largernet_vb_lsr_'+conn_weight+'.py')
		os.remove('largernet_'+conn_weight+'.hoc')

		with open('./compiled/largernet_vb_lsr_'+conn_weight+'.py') as oldver, open('./largernet_vb_lsr_'+conn_weight+'.py','w') as newver:
		    for line in oldver:
		        newver.write(line) 
		with open('./compiled/largernet_'+conn_weight+'.hoc') as oldver, open('./largernet_'+conn_weight+'.hoc','w') as newver:
		    for line in oldver:
		        newver.write(line) 

# deleted the program copy in the main directory TC_model
os.chdir('/Users/jiemei/Desktop/TC_model')
os.remove('largernet_vb_lsr_'+conn_weight+'.py')		
os.remove('largernet_'+conn_weight+'.hoc')

for ii in range(3,7):
	for i in range(0, num_tc_cell):
		tc_results = '/run_lgn_pgn/largernet/'+conn_weight+'/light_spot_'+str(ii)+'/relay/tc_cell'
		os.chdir('/Users/jiemei/Desktop/TC_model'+tc_results+str(i))

		read_files = glob.glob("*.dat")

		with open(tc_results_dat+'tc_cell'+str(i)+'_lsr0'+str(ii)+'.dat', "wb") as outfile:
		    for f in read_files:
		        with open(f, "rb") as infile:
					outfile.write(infile.read())

for ii in range(3,7):
	for i in range(0, num_re_cell):
		re_results = '/run_lgn_pgn/largernet/'+conn_weight+'/light_spot_'+str(ii)+'/reticular/re_cell'
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
		tc_results = './run_lgn_pgn/largernet/'+conn_weight+'/tc_lsr_results'
		if not os.path.exists(tc_results): 
			os.makedirs(tc_results)

		os.chdir(tc_results_dat)
		r = io.AsciiSpikeTrainIO(filename = 'tc_cell'+str(i)+'_lsr0'+str(ii)+'.dat')
		seg = r.read_segment(unit=ms)
		#print seg.spiketrains
		for st in seg.spiketrains:
			st.t_stop = 2400*ms
		tc_plot = es.time_histogram(seg.spiketrains, 20*ms, output='counts')    
		plt.plot(tc_plot)

		os.chdir('/Users/jiemei/Desktop/TC_model/run_lgn_pgn/largernet/'+conn_weight+'/tc_lsr_results')
		plt.savefig('tc_cell'+str(i)+'_lsr0'+str(ii)+'.png')
		plt.close()

for ii in range(3,7):
	re_plot = []
	for i in range(0, num_re_cell):
		os.chdir('/Users/jiemei/Desktop/TC_model')
		re_results = './run_lgn_pgn/largernet/'+conn_weight+'/re_lsr_results'
		if not os.path.exists(re_results): 
			os.makedirs(re_results)
		
		os.chdir(re_results_dat)
		r = io.AsciiSpikeTrainIO(filename = 're_cell'+str(i)+'_lsr0'+str(ii)+'.dat')
		seg = r.read_segment(unit=ms)
		#print seg.spiketrains
		for st in seg.spiketrains:
			st.t_stop = 2400*ms
		re_plot = es.time_histogram(seg.spiketrains, 20*ms, output='counts')    
		plt.plot(re_plot)
		#plt.ylim(0, 30)
		os.chdir('/Users/jiemei/Desktop/TC_model/run_lgn_pgn/largernet/'+conn_weight+'/re_lsr_results')
		plt.savefig('re_cell'+str(i)+'_lsr0'+str(ii)+'.png')
		plt.close()
