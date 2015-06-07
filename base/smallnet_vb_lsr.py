########################################################################
###### this script specifies connectivity between LGN-PGN cells
########################################################################
###### import things
from neuron import h
from sys import argv
import random
from random import randint
import string
import fileinput
import matplotlib.pylab as plt
from matplotlib.artist import setp
from function_connectivity import take_section, all_to_all_connect, one_to_one_connect, data_output, mutual_connect
#from run_trial_v1.py import importing
########################################################################
ncell_tc = 4
ncell_re = 2
ncell_in = 1
ncell_retinal_ganglion = 4
n_condition = 2
########################################################################
file = open(hocfile).read()
#file = file.replace('ncells=2', 'ncells=3')
f = open(hocfile, 'w')
f.write(file)
f.close()
h.load_file(hocfile)
########################################################################
###### making a dictionary contains secname() for proximal_re/distal_re...
relay_morph = open('relay.txt','r')
relay = eval(relay_morph.read())
relay_morph.close() 
reti_morph = open('reticular.txt','r')
reticular = eval(reti_morph.read())
reti_morph.close() 
inter_morph = open('interneuron.txt','r')
interneuron = eval(inter_morph.read())
inter_morph.close() 
retinal_ganglion_morph = open('retinal_ganglion.txt','r')
retinal_ganglion = eval(retinal_ganglion_morph.read())
retinal_ganglion_morph.close() 
#for sect in h.allsec(): 
#		print sect.name()
########################################################################	
###### taking sections to be connected	
soma_tc = take_section(relay, "soma_tc", ncell_tc)
distal_tc = take_section(relay, "distal_tc", ncell_tc)
proximal_tc = take_section(relay, "proximal_tc", ncell_tc)
proximal_re = take_section(reticular, "proximal_re", ncell_re)
distal_in = take_section(interneuron, "distal_in", ncell_in)
soma_tc = take_section(relay, "soma_tc", ncell_tc)
soma_in = take_section(interneuron, "soma_in", ncell_in)
soma_re = take_section(reticular, "soma_re", ncell_re)
medial_re = take_section(reticular, "medial_re", ncell_re)
retinal = take_section(retinal_ganglion, "retinal_ganglion", ncell_retinal_ganglion)
########################################################################	
###### triadic arrangement. this makes sure the triadic structure
triad_tc = []
for i in range (0, ncell_tc):
	triad_tc.append([])
	n_selsect = randint(0, len(proximal_tc[i])-1)
	triad_tc[i].append(proximal_tc[i][n_selsect])

triad_in = []
for i in range (0, ncell_tc):
	triad_in.append([])
	n_selsect = randint(0, len(distal_in[0])-1)
	triad_in[i].append(distal_in[0][n_selsect])
########################################################################	
###### symmetric structure as in LamSherman paper
rgc_tc =  []
rgc_tc = []
syn_rgc_tc = []
rgc_in = []
syn_rgc_in = []
in_tc = []
syn_in_tc =[]
tc_re = []
syn_tc_re =[]
re_tc = []
syn_re_tc = []
re_re = []
syn_re_re = []

one_to_one_connect(rgc_tc, syn_rgc_tc, 'AMPA', retinal, triad_tc, ncell_retinal_ganglion, ncell_tc, 1, cw_rgc_tc, 0)
print '-----------------------------'
one_to_one_connect(rgc_in, syn_rgc_in, 'AMPA', retinal, triad_in, ncell_retinal_ganglion, ncell_tc, 1, cw_rgc_in, 0)
print '-----------------------------'
one_to_one_connect(in_tc, syn_in_tc, 'GABAa', triad_in, triad_tc, ncell_in, ncell_tc, 1, cw_in_tc, -10)
print '-----------------------------'
#all_to_all_connect(tc_re, syn_tc_re, 'AMPA', soma_tc, proximal_re, ncell_tc, ncell_re, 5, cw_tc_re, 0)
all_to_all_connect(tc_re, syn_tc_re, 'AMPA', soma_tc, proximal_re, ncell_tc, ncell_re, 5, cw_tc_re, 0)
print '-----------------------------'
all_to_all_connect(re_tc, syn_re_tc, 'GABAa', soma_re, distal_tc, ncell_re, ncell_tc, 10, cw_re_tc, -15)
print '-----------------------------'
#mutual_connect(re_re, syn_re_re, 'GABAa', medial_re, medial_re, ncell_re, ncell_re, 15, cw_re_re, -15) # uncomment this to use PGN-PGN mutual inhibition

########################################################################	
###### export spike data to file 
vec_dend_tc = {}
for i in range (0, 4):
	for var in 'v_dend_tc'+str(i), 't':
		vec_dend_tc[var] = h.Vector()
	vec_dend_tc['v_dend_tc'+str(i)].record(triad_tc[i][0](0.5)._ref_v)
vec_dend_tc['t'].record(h._ref_t)

vec_soma_tc = {}
for i in range (0, 4):
	for var in 'v_soma_tc'+str(i), 't':
		vec_soma_tc[var] = h.Vector()
	vec_soma_tc['v_soma_tc'+str(i)].record(soma_tc[i][0](0.5)._ref_v)
vec_soma_tc['t'].record(h._ref_t)

vec_soma_re = {}
for i in range (0, 2):
	for var in 'v_soma_re'+str(i), 't':
		vec_soma_re[var] = h.Vector()
	vec_soma_re['v_soma_re'+str(i)].record(soma_re[i][0](0.5)._ref_v)
vec_soma_re['t'].record(h._ref_t)

vec_retinal = {}
for i in range (0, 4):
	for var in 'v_retinal'+str(i), 't':
		vec_retinal[var] = h.Vector()
	vec_retinal['v_retinal'+str(i)].record(retinal[i][0](0.5)._ref_v)
vec_retinal['t'].record(h._ref_t)

h.load_file("stdrun.hoc")
h.init()
h.tstop = 2500
h.run()

for i in range(0, n_tc_cell):
	directory_tc = dir_tc+str(i)+'/'
	data_output(directory_tc, 'tc_cell'+str(i)+'_lsr'+str(condition_id)+'_0'+str(trial_id), vec_soma_tc, 'v_soma_tc'+str(i))
for i in range(0, n_re_cell):
	directory_re = dir_re+str(i)+'/'
	data_output(directory_re, 're_cell'+str(i)+'_lsr'+str(condition_id)+'_0'+str(trial_id), vec_soma_re, 'v_soma_re'+str(i))
########################################################################	