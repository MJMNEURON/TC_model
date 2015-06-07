
########################################################################
###### this script:
###### 1. specifies connectivity between LGN-PGN cells
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
from function_connectivity import take_section, all_to_all_connect, one_to_one_connect, some_to_some_connect, data_output
#from run_trial_v1.py import importing
########################################################################
ncell_tc = 16
ncell_re = 12
ncell_in = 4
ncell_retinal_ganglion = 16
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
retinal = take_section(retinal_ganglion, "retinal_ganglion", ncell_retinal_ganglion)
'''
print proximal_tc
print 'len_proximal_tc'+str(len(proximal_tc))
print 'len(proximal_tc[3])'+str(len(proximal_tc[3]))
print proximal_re
print 'len(proximal_re[0])'+str(len(proximal_re[0]))
'''
########################################################################	
###### triadic arrangement. this makes sure the triadic structure
triad_tc = []
for i in range (0, ncell_tc):
	triad_tc.append([])
	n_selsect = randint(0, len(proximal_tc[i])-1)
	triad_tc[i].append(proximal_tc[i][n_selsect])
'''
triad_in = []
for i in range (0, ncell_tc):
	triad_in.append([])
	n_selsect = randint(0, len(distal_in[0])-1)
	triad_in[i].append(distal_in[0][n_selsect])
'''
triad_in = []
for i in range (0, ncell_in):
	triad_in.append([])
	for ii in range (0, ncell_tc/ncell_in):
		n_selsect = randint(0, len(distal_in[i])-1)
		triad_in[i].append(distal_in[i][n_selsect])
########################################################################	
###### symmetric structure as in LamSherman paper
'''
soma_tc_left = []
soma_tc_right = []

numbers = [0, 1]
for i in range (0, 1):	
	n_select = numbers[randint(0, len(numbers)-1)]
	soma_tc_left.append(soma_tc[n_select])
	#numbers.remove(n_select)

numbers = [2, 3]
for i in range (0, 1):	
	n_select = numbers[randint(0, len(numbers)-1)]
	soma_tc_left.append(soma_tc[n_select])
	#numbers.remove(n_select)

for x in soma_tc:
	soma_tc_right.append(x)
for x in soma_tc_left:
	soma_tc_right.remove(x)
'''
rgc_tc =  []
syn_rgc_tc = []
rgc_in = []
syn_rgc_in = []
in_tc = []
syn_in_tc = []
tc_re = []
syn_tc_re = []
re_tc = []
syn_re_tc = []
'''
proximal_re_left = []
proximal_re_right = []
proximal_re_left.append(proximal_re[0])
proximal_re_right.append(proximal_re[1])
'''
#                 (connection, syn, receptor, sender, receiver, ratio1, ratio2, n_synapse, conn_weight, threshold)
one_to_one_connect(rgc_tc, syn_rgc_tc, 'AMPA', retinal, triad_tc, ncell_retinal_ganglion, ncell_tc, 1, cw_rgc_tc, 0)
print '-----------------------------'
some_to_some_connect(rgc_in, syn_rgc_in, 'AMPA', retinal, triad_in, ncell_retinal_ganglion, ncell_in, 1, cw_rgc_in, 0)
print '-----------------------------'
some_to_some_connect(in_tc, syn_in_tc, 'GABAa', triad_in, triad_tc, ncell_in, ncell_tc, 1, cw_in_tc, -10)
print '-----------------------------'
#all_to_all_connect(tc_re, syn_tc_re, 'AMPA', soma_tc, proximal_re, ncell_tc, ncell_re, 5, cw_tc_re, 0)
all_to_all_connect(tc_re, syn_tc_re, 'AMPA', soma_tc, proximal_re, ncell_tc, ncell_re, 5, cw_tc_re, 0)
print '-----------------------------'
all_to_all_connect(re_tc, syn_re_tc, 'GABAa', soma_re, distal_tc, ncell_re, ncell_tc, 10, cw_re_tc, -15)
########################################################################	
###### export spike data to file 
vec_dend_tc = {}
for i in range (0, ncell_tc):
	for var in 'v_dend_tc'+str(i), 't':
		vec_dend_tc[var] = h.Vector()
	vec_dend_tc['v_dend_tc'+str(i)].record(triad_tc[i][0](0.5)._ref_v)
vec_dend_tc['t'].record(h._ref_t)

vec_soma_tc = {}
for i in range (0, ncell_tc):
	for var in 'v_soma_tc'+str(i), 't':
		vec_soma_tc[var] = h.Vector()
	vec_soma_tc['v_soma_tc'+str(i)].record(soma_tc[i][0](0.5)._ref_v)
vec_soma_tc['t'].record(h._ref_t)

vec_soma_re = {}
for i in range (0, ncell_re):
	for var in 'v_soma_re'+str(i), 't':
		vec_soma_re[var] = h.Vector()
	vec_soma_re['v_soma_re'+str(i)].record(soma_re[i][0](0.5)._ref_v)
vec_soma_re['t'].record(h._ref_t)

vec_retinal = {}
for i in range (0, ncell_retinal_ganglion):
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
	data_output(directory_tc, 'tc_cell'+str(i)+'_csr'+str(int(condition_id))+'_0'+str(trial_id), vec_soma_tc, 'v_soma_tc'+str(i))
for i in range(0, n_re_cell):
	directory_re = dir_re+str(i)+'/'
	data_output(directory_re, 're_cell'+str(i)+'_csr'+str(int(condition_id))+'_0'+str(trial_id), vec_soma_re, 'v_soma_re'+str(i))
########################################################################	
###### plotting
'''
for i in range(0, 4):
	plt.xlabel('t (ms)')
	plt.ylabel('v (mV)') 
	plt.subplot(4,2,i+1)
	lines = plt.plot(vec_dend_tc['t'], vec_dend_tc['v_dend_tc'+str(i)], label=str(i)+': '+triad_tc[i][0].name() )
	setp(lines, linewidth=0.5, color='b')
	plt.legend(loc='upper left', prop={'size':10})
	plt.xlim(0, 2500)
	plt.ylim(-80, 40)

for i in range(0, 4):
	plt.xlabel('t (ms)')
	plt.ylabel('v (mV)') 
	plt.subplot(4,2,i+5)
	lines = plt.plot(vec_soma_tc['t'], vec_soma_tc['v_soma_tc'+str(i)], label=str(i)+': '+soma_tc[i][0].name() )
	setp(lines, linewidth=0.5, color='r')
	plt.legend(loc='upper left', prop={'size':10})
	plt.xlim(0, 2500)
	plt.ylim(-80, 40)
plt.show()

for i in range(0, 2):
	plt.xlabel('t (ms)')
	plt.ylabel('v (mV)') 
	plt.subplot(2,2,i+3)
	lines = plt.plot(vec_soma_tc['t'], vec_soma_tc['v_soma_tc'+str(i)], label=str(i)+': '+soma_tc[i][0].name() )
	setp(lines, linewidth=0.5, color='b')
	plt.legend(loc='upper left', prop={'size':10})
	plt.xlim(0, 2500)
	plt.ylim(-80, 40)

for i in range(0, 2):
	plt.xlabel('t (ms)')
	plt.ylabel('v (mV)') 
	plt.subplot(2,2,i+1)
	lines = plt.plot(vec_soma_re['t'], vec_soma_re['v_soma_re'+str(i)], label=str(i)+': '+soma_re[i][0].name() )
	setp(lines, linewidth=0.5, color='r')
	plt.legend(loc='upper left', prop={'size':10})
	plt.xlim(0, 2500)
	plt.ylim(-80, 40)
plt.show()
'''