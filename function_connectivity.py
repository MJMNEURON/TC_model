########################################################################
from neuron import h
import random
from random import randint
import os
import glob
########################################################################
###### taking sections of a specific cell type from all sections
###### e.g., distal/proximal/medial dendritic sections from relay cell
def take_section(cell_name, key_name, ncell):
	cell = []
	cellname =[]
	section = []
	section_name = []
	for sect in h.allsec(): 
		if any(s in sect.name() for s in cell_name[key_name]):			
			section.append(sect)
			section_name.append(sect.name())
	for i in range (0, ncell):
		cell.append([])
		cellname.append([])
		char = 'cell['+str(i)+']'
		for sects in section:
			if (char in sects.name()):
				cell[i].append(sects)
				cellname[i].append(sects.name())

	print 'key', key_name
	print '------------------------------------------------------'
	return cell #, cellname
########################################################################
def all_to_all_connect(connection, syn, receptor, sender, receiver, ratio1, ratio2, n_synapse, conn_weight, threshold):
	selsend=[]
	selrece=[]
	for iiii in range(0, ratio1*ratio2):
		selsend.append([])
		selrece.append([])
	for i in range (1, ratio1+1):
		send = sender[i-1]
		for iii in range (1, ratio2+1):
			receive = receiver[iii-1]
			for ii in range (0, n_synapse):
				n_sender = randint(0, len(send)-1)
				selsend[ratio2*(i-1)-1+iii].append(send[n_sender])
				n_receiver = randint(0, len(receive)-1)
				selrece[ratio2*(i-1)-1+iii].append(receive[n_receiver])
				if (receptor == 'AMPA'):
					syn_n = h.AMPA(0.5, sec = selrece[ratio2*(i-1)-1+iii][ii])
					syn.append(syn_n)
				if (receptor == 'GABAa'):
					syn_n = h.GABAa(0.5, sec = selrece[ratio2*(i-1)-1+iii][ii])
					syn.append(syn_n)
				connection_n=h.NetCon(selsend[ratio2*(i-1)-1+iii][ii](0.5)._ref_v, syn_n, sec = selsend[ratio2*(i-1)-1+iii][ii])
				connection_n.weight[0] = conn_weight
				connection_n.threshold = threshold
				connection.append(connection_n)
				print '-----------------------------'
				print "sender[" + str(ratio2*(i-1)-1+iii) + '][' + str(ii)+ "]= ", selsend[ratio2*(i-1)-1+iii][ii].name()
				print "receiver[" + str(ratio2*(i-1)-1+iii) + '][' + str(ii)+ "]= ", selrece[ratio2*(i-1)-1+iii][ii].name()				
	print '------------------------------------------------------'''
#	print selsend
print '------------------------------------------------------'''
########################################################################
# previous version when there's only one interneuron
def one_to_one_connect(connection, syn, receptor, sender, receiver, ratio1, ratio2, n_synapse, conn_weight, threshold):
	for i in range(0, len(sender)):
		send = sender[i]
		receive = receiver[i]
		if (receptor == 'AMPA'):
			syn_n = h.AMPA(0.5, sec = receive[0])
			syn.append(syn_n)
		if (receptor == 'GABAa'):
			syn_n = h.GABAa(0.5, sec = receive[0])
			syn.append(syn_n)
		connection_n=h.NetCon(send[0](0.5)._ref_v, syn_n, sec = send[0])
		connection_n.weight[0] = conn_weight
		connection_n.threshold = threshold
		connection.append(connection_n)
		print '-----------------------------'
		print "sender[" + str(i) + ']', send[0].name()
		print "receiver[" + str(i) + ']', receive[0].name()	
########################################################################
def some_to_some_connect(connection, syn, receptor, sender, receiver, ratio1, ratio2, n_synapse, conn_weight, threshold):
	if (ratio1 > ratio2):
		larger = ratio1
		smaller = ratio2
		ratio = larger/smaller
		for ii in range (0, smaller):
			for i in range(0, ratio):
				#n_sender = randint(0, len(sender[i])-1)
				send = sender[ii*ratio+i][0]
				#n_receiver = randint(0, len(receiver[ii])-1)
				receive = receiver[ii][i]
				if (receptor == 'AMPA'):
					syn_n = h.AMPA(0.5, sec = receive)
					syn.append(syn_n)
				if (receptor == 'GABAa'):
					syn_n = h.GABAa(0.5, sec = receive)
					syn.append(syn_n)
				connection_n=h.NetCon(send(0.5)._ref_v, syn_n, sec = send)
				connection_n.weight[0] = conn_weight
				connection_n.threshold = threshold
				connection.append(connection_n)
				print '-----------------------------'
				print "sender[" + str(i) + ']', send.name()
				print "receiver[" + str(i) + ']', receive.name()	
	else:
		larger = ratio2
		smaller = ratio1
		ratio = larger/smaller
		for ii in range (0, smaller):
			for i in range(0, ratio):
				send = sender[ii][i]
				receive = receiver[ii*ratio+i][0]
				if (receptor == 'AMPA'):
					syn_n = h.AMPA(0.5, sec = receive)
					syn.append(syn_n)
				if (receptor == 'GABAa'):
					syn_n = h.GABAa(0.5, sec = receive)
					syn.append(syn_n)
				connection_n=h.NetCon(send(0.5)._ref_v, syn_n, sec = send)
				connection_n.weight[0] = conn_weight
				connection_n.threshold = threshold
				connection.append(connection_n)
				print '-----------------------------'
				print "sender[" + str(i) + ']', send.name()
				print "receiver[" + str(i) + ']', receive.name()	
########################################################################
###### mutual inhibition between PGN reticular cells
def mutual_connect(connection, syn, receptor, sender, receiver, ratio1, ratio2, n_synapse, conn_weight, threshold):
	for i in range(0, len(sender)-1):
		for ii in range (0, n_synapse):
			send1 = sender[i]
			receive1 =  sender[i+1]
			n_sender = randint(0, len(send1)-1)
			n_receiver = randint(0, len(receive1)-1)
			if (receptor == 'AMPA'):
				syn_n = h.AMPA(0.5, sec = receive1[n_receiver])
				syn.append(syn_n)
			if (receptor == 'GABAa'):
				syn_n = h.GABAa(0.5, sec = receive1[n_receiver])
				syn.append(syn_n)
			connection_n=h.NetCon(send1[n_sender](0.5)._ref_v, syn_n, sec = send1[n_sender])
			connection_n.weight[0] = conn_weight
			connection_n.threshold = threshold
			connection.append(connection_n)
			print '-----------------------------'
			print "sender[" + str(i) + ']', send1[n_sender].name()
			print "receiver[" + str(i) + ']', receive1[n_receiver].name()	

		for ii in range (0, n_synapse):
			send2 = sender[i+1]
			receive2 = sender[i]
			n_sender = randint(0, len(send2)-1)
			n_receiver = randint(0, len(receive2)-1)
			if (receptor == 'AMPA'):
				syn_n = h.AMPA(0.5, sec = receive2[n_receiver])
				syn.append(syn_n)
			if (receptor == 'GABAa'):
				syn_n = h.GABAa(0.5, sec = receive2[n_receiver])
				syn.append(syn_n)
			connection_n=h.NetCon(send2[n_sender](0.5)._ref_v, syn_n, sec = send2[n_sender])
			connection_n.weight[0] = conn_weight
			connection_n.threshold = threshold
			connection.append(connection_n)
			print '-----------------------------'
			print "sender[" + str(i) + ']', send2[n_sender].name()
			print "receiver[" + str(i) + ']', receive2[n_receiver].name()
########################################################################
###### generate Poisson-driven spike trains
###### connect those with target cells in LGN-PGN
def cortical_connect(connection, syn, receptor, sender, receiver, amount_receiver, n_synapse, conn_weight, threshold, time, id):
	for i in range(0, amount_receiver):		
		sender.append([])
		receive = receiver[i]

		for ii in range(0, n_synapse):
			syn_s = h.NetStim(0.5) # receiver
			syn_s.interval=30 # =1000/f, f is the mean frequency of activation in Hz
			syn_s.number=80
			syn_s.start=100
			syn_s.noise=1
			sender[i].append(syn_s)	

			n_receiver = randint(0, len(receive)-1)
			if (receptor == 'AMPA'):
				syn_n = h.AMPA(0.5, sec = receive[n_receiver])
				syn.append(syn_n)
			if (receptor == 'GABAa'):
				syn_n = h.GABAa(0.5, sec = receive[n_receiver])
				syn.append(syn_n)

			connection_n=h.NetCon(sender[i][ii], syn_n) 
			connection_n.weight[0] = conn_weight
			connection_n.threshold = threshold
			
			#print len(receiver)
			print '-----------------------------'
			print "receiver[" + str(i) + ']', receive[n_receiver].name()

			connection_n.record(time[i], id[i], ii+1)
			connection.append(connection_n)
			#print len(sender)
########################################################################
###### save data
def data_output(directory, cellname, vecname, varname):
	total = 0
	timestep = 0
	print '-----'+ cellname +' ------'
	#with open('data/'+cellname+'.dat', 'w') as file_to_write:
	'''
	os.chdir(directory)
	files = glob.glob("*.dat")
	for f in files:
	    os.remove(f)
	'''
	with open(directory+cellname+'.dat', 'w') as file_to_write:
		for i in range(0, int(vecname['t'].size())): #print h.vec.size() 
		    if ( vecname[varname].x[i] >= -15 and timestep + 1 < vecname['t'].x[i]): 
				timestep=vecname['t'].x[i]
				total=total+1
				print total
				print timestep
				file_to_write.write(str(timestep)+'\n')
		print str(total/2.5) + 'Hz'
########################################################################