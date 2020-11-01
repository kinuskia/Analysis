import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker


#percentiles = np.arange(100)
p = 0

# Read in IPSM fit result

centrality_class =  str(p) + '-' + str(p+1)
filename_fit = "../IPSM-Fit/output/" + centrality_class + ".txt"
One_sw2_N, sn2_N_N2 = np.loadtxt(filename_fit, unpack=True)


modes = [0, 1, 2, 3, 4]
lMax = 6

# Set up figure and image grid
figs, axs = plt.subplots(4, len(modes), figsize=(8.0,6.0),sharex="col", sharey="row", constrained_layout=True)



# Find maximal correlator value
maximal_value_Trento = 0
maximal_value_CGC = 0
maximal_value_Nc = 0
maximal_value_IPSM = 0
for mode in modes:
	#import two-point functions
	source = 'output/two_point_random_' + str(p) + '-' + str(p+1) + '_m' + str(mode) + '_real' +'.txt'
	profile = np.loadtxt(source)
	# import one-point functions
	source_one = 'output/one_point_' + str(p) + '-' + str(p+1)  +'.txt'
	profile_one_ml = np.loadtxt(source_one)
	# subtract disconnected part from m=0 mode
	if (mode == 0):
		profile[0,0] -= profile_one_ml[mode, 0] * profile_one_ml[mode, 0]

	current_max_Trento = max(np.amax(profile[:lMax,:lMax]), -np.amin(profile[:lMax,:lMax]))
	if (current_max_Trento > maximal_value_Trento):
		maximal_value_Trento = current_max_Trento
	# import CGC simple profiles
	source = 'Saclay_simplified/output/'+centrality_class+'/two_point_random_connected' + '_m_' + str(mode)  +'.txt'
	profile = np.loadtxt(source)
	# # add geometry part
	# source_one_point = 'output/one_point_'+centrality_class+'.txt'
	# one_points = np.loadtxt(source_one_point)
	# for i in range(0, lMax):
	# 	for j in range(0, lMax):
	# 		if ((i==0)&(j==0)&(mode==0)):
	# 			profile[i][j] += 1./np.pi/np.pi*(sn2_N_N2)
	# 		else:
	# 			profile[i][j] += (1.+sn2_N_N2)*one_points[mode, i]*one_points[mode, j]
					
	current_max_CGC = max(np.amax(profile[:lMax,:lMax]), -np.amin(profile[:lMax,:lMax]))
	if (current_max_CGC > maximal_value_CGC):
		maximal_value_CGC = current_max_CGC
	#import Large_Nc profile
	source = 'Saclay/output/'+centrality_class+'/Nr41/Nm64/m5.0e-3/two_point_random_connected' + '_m_' + str(mode)  +'.txt'
	profile = np.loadtxt(source)
	# # add geometry part
	# source_one_point = 'output/one_point_'+centrality_class+'.txt'
	# one_points = np.loadtxt(source_one_point)
	# for i in range(0, lMax):
	# 	for j in range(0, lMax):
	# 		if ((i==0)&(j==0)&(mode==0)):
	# 			profile[i][j] += 1./np.pi/np.pi*(sn2_N_N2)
	# 		else:
	# 			profile[i][j] += (1.+sn2_N_N2)*one_points[mode, i]*one_points[mode, j]

	current_max_Nc = max(np.amax(profile[:lMax,:lMax]), -np.amin(profile[:lMax,:lMax]))
	if (current_max_Nc > maximal_value_Nc):
		maximal_value_Nc = current_max_Nc
	#import IPSM profile
	source_one_point = 'output/one_point_'+centrality_class+'.txt'
	one_points = np.loadtxt(source_one_point)
	profile = np.zeros((lMax, lMax))
	clm_old = np.loadtxt("output/clm.txt")
	clm = np.zeros((lMax, len(modes)))
	for l in range(0, lMax):
		for m in range(0, len(modes)):
			if ((m==0)):
				if (l==0):
					clm[l][m] = 1./2
				else:
					clm[l][m] = clm_old[l-1][m]
			else:
				clm[l][m] = clm_old[l][m]
	for i in range(0, lMax):
		for j in range(0, lMax):
			if ((i == 0)&(j==0)&(mode == 0)):
				profile[i][j] = 1./np.pi/np.pi*(One_sw2_N+sn2_N_N2)
			elif ((i == j)):
				profile[i][j] = (-1.0)**mode/2./np.pi**2/clm[i, mode]*One_sw2_N + (1.+sn2_N_N2)*one_points[mode, i]*one_points[mode, j]
			else:
				profile[i][j] = (1.+sn2_N_N2)*one_points[mode, i]*one_points[mode, j]
	current_max_IPSM = max(np.amax(profile[:lMax,:lMax]), -np.amin(profile[:lMax,:lMax]))
	if (current_max_IPSM > maximal_value_IPSM):
		maximal_value_IPSM = current_max_IPSM
print("Trento: ", maximal_value_Trento)
print("CGC: ", maximal_value_CGC)
print("Nc: ", maximal_value_Nc)
print("IPSM: ", maximal_value_IPSM)

maximal_TN = max(maximal_value_Trento, maximal_value_Nc)
maximal_IC = max(maximal_value_CGC, maximal_value_IPSM)
maximal_T = maximal_TN
maximal_N = maximal_TN
maximal_I = maximal_IC
maximal_C = maximal_IC

# maximal_T = maximal_value_Trento
# maximal_N = maximal_value_Nc
# maximal_I = maximal_value_IPSM
# maximal_C = maximal_value_CGC

cmap_Trento = plt.cm.RdBu
cmap_LargeNc = plt.cm.RdBu
cmap_IPSM = plt.cm.PRGn
cmap_magma = plt.cm.PRGn


from matplotlib.ticker import MaxNLocator
#for ax in axs:
# axs.xaxis.set_major_locator(MaxNLocator(integer=True))
# axs.yaxis.set_major_locator(MaxNLocator(integer=True))

# counter_fig = 0
# plot Trento diagrams
for mode in modes:
	#import two-point functions
	source = 'output/two_point_random_' + str(p) + '-' + str(p+1) + '_m' + str(mode) + '_real' +'.txt'
	profile = np.loadtxt(source)
	# import one-point functions
	source_one = 'output/one_point_' + str(p) + '-' + str(p+1)  +'.txt'
	profile_one_ml = np.loadtxt(source_one)
	# subtract disconnected part from m=0 mode
	if (mode == 0):
		profile[0,0] -= profile_one_ml[mode, 0] * profile_one_ml[mode, 0]

	im1 = axs[0][mode].imshow(profile[0:(lMax),0:(lMax)], interpolation=None, cmap=cmap_Trento, vmin = -maximal_T, vmax = maximal_T, extent = (-0.5+1, len(profile[0,0:(lMax)])-0.5+1, len(profile[0:(lMax),0])-0.5+1, -0.5+1))
	#centrality_class =  str(p) + '-' + str(p+1) + '%'
	#if (mode == 0):
		#axs[mode][0].set_title("TRENTo")
		
	axs[0][mode].set_title("$m={0}$".format(mode))
	axs[3][mode].set_xlabel("$l_2$")
	axs[0][mode].set_xticks(np.arange(lMax)+1)
	axs[0][mode].set_yticks(np.arange(lMax)+1)


	# # colorbar
	# if (mode == modes[-1]):
	# 	short = axs[mode][0].cax
	# 	short.colorbar(im)
	# 	tick_T = float('%.1g' % (maximal_T*0.6))
	# 	short.set_xticks([-tick_T, tick_T])
	# 	short.toggle_label(True)

	# counter_fig = counter_fig + 1

# plot Saclay diagrams
for mode in modes:
	#import two-point functions
	source = 'Saclay/output/'+centrality_class+'/Nr41/Nm64/m5.0e-3/two_point_random_connected' + '_m_' + str(mode)  +'.txt'
	profile = np.loadtxt(source)
	# # add geometry part
	# source_one_point = 'output/one_point_'+centrality_class+'.txt'
	# one_points = np.loadtxt(source_one_point)
	# for i in range(0, lMax):
	# 	for j in range(0, lMax):
	# 		if ((i==0)&(j==0)&(mode==0)):
	# 			profile[i][j] += 1./np.pi/np.pi*(sn2_N_N2)
	# 		else:
	# 			profile[i][j] += (1.+sn2_N_N2)*one_points[mode, i]*one_points[mode, j]

	axs[1][mode].imshow(profile[0:(lMax),0:(lMax)], interpolation=None, cmap=cmap_LargeNc, vmin = -maximal_N, vmax = maximal_N, extent = (-0.5+1, len(profile[0,0:(lMax)])-0.5+1, len(profile[0:(lMax),0])-0.5+1, -0.5+1))
	#centrality_class =  str(p) + '-' + str(p+1) + '%'
	#if (mode == 0):
		#axs[1][mode].set_title("Large $N_c$")
	#if (mode == modes[-1]):
		#axs[mode][1].set_xlabel("$l_2$")
	axs[1][mode].set_xticks(np.arange(lMax)+1)
	axs[1][mode].set_yticks(np.arange(lMax)+1)
	#ax.set_ylabel("$m={0}$\n$l_1$".format(mode))

	# # colorbar
	# if (mode == modes[-1]):
	# 	short = axs[mode][1].cax
	# 	short.colorbar(im)
	# 	tick_N = float('%.1g' % (maximal_N*0.6))
	# 	short.set_xticks([-tick_N, tick_N])
	# 	short.toggle_label(True)



# plot IPSM diagrams 
for mode in modes:
	#import one-point functions
	source_one_point = 'output/one_point_'+centrality_class+'.txt'
	one_points = np.loadtxt(source_one_point)
	profile = np.zeros((lMax, lMax))

	clm_old = np.loadtxt("output/clm.txt")
	clm = np.zeros((lMax, len(modes)))
	for l in range(0, lMax):
		for m in range(0, len(modes)):
			if ((m==0)):
				if (l==0):
					clm[l][m] = 1./2
				else:
					clm[l][m] = clm_old[l-1][m]
			else:
				clm[l][m] = clm_old[l][m]

	for i in range(0, lMax):
		for j in range(0, lMax):
			if ((i == 0)&(j==0)&(mode == 0)):
				profile[i][j] = 1./np.pi/np.pi*(One_sw2_N+sn2_N_N2)
			elif ((i == j)):
				profile[i][j] = (-1.0)**mode/2./np.pi**2/clm[i, mode]*One_sw2_N + (1.+sn2_N_N2)*one_points[mode, i]*one_points[mode, j]
			else:
				profile[i][j] = (1.+sn2_N_N2)*one_points[mode, i]*one_points[mode, j]


	im2 = axs[2][mode].imshow(profile[0:(lMax),0:(lMax)], interpolation=None, cmap=cmap_IPSM, vmin = -maximal_I, vmax = maximal_I, extent = (-0.5+1, len(profile[0,0:(lMax)])-0.5+1, len(profile[0:(lMax),0])-0.5+1, -0.5+1))
	#centrality_class =  str(p) + '-' + str(p+1) + '%'
	#if (mode == 0):
		#axs[mode][2].set_title("IPSM")
	#if (mode == modes[-1]):
		#axs[mode][2].set_xlabel("$l_2$")
		#figs.colorbar(im2, ax = axs[2:4][mode], location = "right", shrink = 1, pad=0.0, aspect = 40)
	axs[2][mode].set_xticks(np.arange(lMax)+1)
	axs[2][mode].set_yticks(np.arange(lMax)+1)
	#ax.set_ylabel("$m={0}$\n$l_1$".format(mode))

	# # colorbar
	# if (mode == modes[-1]):
	# 	short = axs[mode][2].cax
	# 	short.colorbar(im)
	# 	tick_I = float('%.1g' % (maximal_I*0.6))
	# 	short.set_xticks([-tick_I, tick_I])
	# 	short.toggle_label(True)


# plot Saclay simple diagrams
for mode in modes:
	#import two-point functions
	source = 'Saclay_simplified/output/'+centrality_class+'/two_point_random_connected' + '_m_' + str(mode)  +'.txt'
	profile = np.loadtxt(source)
	# # add geometry part
	# source_one_point = 'output/one_point_'+centrality_class+'.txt'
	# one_points = np.loadtxt(source_one_point)
	# for i in range(0, lMax):
	# 	for j in range(0, lMax):
	# 		if ((i==0)&(j==0)&(mode==0)):
	# 			profile[i][j] += 1./np.pi/np.pi*(sn2_N_N2)
	# 		else:
	# 			profile[i][j] += (1.+sn2_N_N2)*one_points[mode, i]*one_points[mode, j]

	axs[3][mode].imshow(profile[0:(lMax),0:(lMax)], interpolation=None, cmap=cmap_magma, vmin = -maximal_C, vmax = maximal_C, extent = (-0.5+1, len(profile[0,0:(lMax)])-0.5+1, len(profile[0:(lMax),0])-0.5+1, -0.5+1))
	#centrality_class =  str(p) + '-' + str(p+1) + '%'
	#if (mode == 0):
		#axs[mode][3].set_title("magma")
	#if (mode == modes[-1]):
		#axs[mode][3].set_xlabel("$l_2$")
	axs[3][mode].set_xticks(np.arange(lMax)+1)
	axs[3][mode].set_yticks(np.arange(lMax)+1)
	#axs[mode][3].set_ylabel("$m={0}$\n$l_1$".format(mode))

	# # colorbar
	# if (mode == modes[-1]):
	# 	short = axs[mode][3].cax
	# 	short.colorbar(im)
	# 	tick_C = float('%.1g' % (maximal_C*0.6))
	# 	short.set_xticks([-tick_C, tick_C])
	# 	short.toggle_label(True)

	cb1 = figs.colorbar(im1, ax = axs[0:2,4], shrink = 1, pad=0.0, aspect = 40, location = "right")
	tick_locator = ticker.MaxNLocator(nbins=5)
	cb1.locator = tick_locator
	cb1.update_ticks()
	figs.colorbar(im2, ax = axs[2:4,4], shrink = 1, pad=0.0, aspect = 40, location = "right")
	axs[0][0].set_ylabel("TrENTo\n$l_1$")
	axs[1][0].set_ylabel("CGC large-$N_c$\n$l_1$")
	axs[2][0].set_ylabel("IPSM\n$l_1$")
	axs[3][0].set_ylabel("magma\n$l_1$")


	#figs.suptitle("$G_{l_1, l_2}^{(m,-m)}$, "+centrality_class+"% class", x=0.5, y=1.05, fontsize=14)

	filename = "plots/two_point_comparison_horizontal_talk_"+centrality_class+".pdf"
	#plt.subplots_adjust(wspace=0.05, hspace=0.05)
	plt.savefig(filename, format='pdf', bbox_inches = "tight")



