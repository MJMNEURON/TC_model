from PIL import Image
import numpy
import glob
import os
import shutil
###############################
# READ spikes.spk
# we want to have a dictionary containing, for each id, the list of spikes

cells = ['1537']

for ls_condition in range (1, 3):
	for cell_id in range (0, 1):
		if ls_condition == 1:
			con_number = '000'
		if ls_condition == 2:
			con_number = '010'
		if ls_condition == 3:
			con_number = '040'
		if ls_condition == 4:
			con_number = '100'	
		'''
		#remove all the files, be careful
		os.chdir('/Users/jiemei/Desktop/TC_model/contrast/csr'+con_number+'/csr'+con_number+'_rgccell_'+cells[cell_id]) 
		files = glob.glob("*.dat")
		for f in files:
		    os.remove(f)
		'''

		#save_data = '/Users/jiemei/Desktop/TC_model/lightspot/lsr0'+con_number+'/lsr0'+con_number+'_rgccell_'+cells[cell_id]
		save_data = '/Users/jiemei/Desktop/TC_model/contrast/csr'+con_number+'/csr'+con_number+'_rgccell_'+cells[cell_id]

		if not os.path.exists(save_data): 
			os.makedirs(save_data)

		for i in range (1, 6):
			#os.chdir('/Users/jiemei/Desktop/TC_model/virtual_retina/spk_original/lsr0'+con_number)
			os.chdir('/Users/jiemei/Desktop/TC_model/virtual_retina/spk_original/csr'+con_number)
			#os.chdir('spk_original')
			retina = {} # output dictionary for spikes

			#vrfile = open('spikes_0'+str(i)+'.spk')
			vrfile = open('spikes_0'+str(i)+'.spk')

			lines = [line.split() for line in vrfile]
			for l in lines:
				# create an array for each cell id
				retina[ l[0] ] = []

			for l in lines:
				if (0.48<float(l[1])<1.92): # USE THIS WHEN GENERATE STIMULI FOR CONTRAST
					retina[ l[0] ].append(float(l[1]))

			# for key in sorted(retina):
			#  	print key, retina[key]
			#print "test 1276"
			#os.chdir('/Users/jiemei/Desktop/TC_model/lightspot/lsr0'+con_number+'/lsr0'+con_number+'_rgccell_'+cells[cell_id])
			os.chdir('/Users/jiemei/Desktop/TC_model/contrast/csr'+con_number+'/csr'+con_number+'_rgccell_'+cells[cell_id])
			
			#with open('lsr0'+con_number+'_rgccell_'+cells[cell_id]+'_0'+str(i)+'.dat', 'w') as file_to_write:
			with open('csr'+con_number+'_rgccell_'+cells[cell_id]+'_0'+str(i)+'.dat', 'w') as file_to_write:
				for i in range(0, len(retina[cells[cell_id]])):
					file_to_write.write(str(retina[cells[cell_id]][i])+'\n')
				print retina[cells[cell_id]]

		os.chdir('/Users/jiemei/Desktop/TC_model/contrast/csr'+con_number+'/csr'+con_number+'_rgccell_'+cells[cell_id]) 

		read_files = glob.glob("*.dat")
		with open('results_rgccell'+cells[cell_id]+'_csr'+con_number+'_20trials.dat', "wb") as outfile:
		    for f in read_files:
		        with open(f, "rb") as infile:
		            outfile.write(infile.read())
'''
###############################
# IMAGES
# Create a png for each timestep
# http://jehiah.cz/a/creating-images-with-numpy

# Virtualetina is by default having 80x80 cells
w,h = 52, 52 ## this is the size image we want to create

# the time span depends on the virtualetina settings
for t in range(800, 1600): # the first 10ms are discarded
	# X On cells
	img_XOn = numpy.empty( (w,h), numpy.uint32 )
	img_XOn.shape = h,w
	img_XOn.fill(0xFFFFFFFF) # fill in solid white by default (0x00000000 for black)
	# X Off cells
	img_XOff = numpy.empty( (w,h), numpy.uint32 )
	img_XOff.shape = h,w
	img_XOff.fill(0xFFFFFFFF) # fill in solid white by default (0x00000000 for black)
	# take the spikes from virtualetina and fill with black the corresponding pixel
	for key in sorted(retina):
		# if the current cell id has a spike in this timestep
		if t in retina[key]:
			# convert virtualetina id in 2D coordinates
			if int(key) < w*w:
				# X On
				xoffset = int(key)/w
				yoffset = int(key)%w
				# print key, xoffset, yoffset
				# img[ startrow:finishrow+1, starx:endx]
				img_XOn[xoffset, yoffset]=0xFF000000
			else:
				# X Off
				k = int(key)-(w*w)
				xoffset = k/w
				yoffset = k%w
				# print key, xoffset, yoffset
				img_XOff[xoffset, yoffset]=0xFF000000				
	# create images from buffer for this timestep
	pilImage = Image.frombuffer('RGBA', (w,h), img_XOn, 'raw', 'RGBA', 0, 1)
	pilImage.save('XOn_frame%d.png' %(t))
	pilImage = Image.frombuffer('RGBA', (w,h), img_XOff, 'raw', 'RGBA', 0, 1)
	pilImage.save('XOff_frame%d.png' %(t))
'''