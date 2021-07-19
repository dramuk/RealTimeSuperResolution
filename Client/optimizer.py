import sys
import os
import cv2
from sklearn.preprocessing import normalize
import numpy as np
import json

"""
Assumption :
1. Time for downscaling is neglible
2. Only significant time is from sending over the network, and the compute (upscaling)
3. Quality Metric average loss for a particular strategy is close to actual loss
4. Assuming bandwidth constant
5. Assuming continuous streaming, and using full FuP per month
6. Assuming computation and network bandwidth reduction factors to be constant for each strategy
7. Assuming renewal everytime FuP is reached
8. If FuP is reached, then plan is renewed
9. Working w/ 720p 
# Cost per hour of compute in dollars
# Cost per GB of storage per month 

Optimizing
Step 1. Find time for compute, network
Step 1.5 Find total time
Step 2. Ask user for how long it'd be stored
Step 3. Find compute/hour ($), MB/s ($), Storage/time ($)
Step 4. Total Cost = sum of all this
Step 5. Per strategy, we have costs
Step 6. From step 1.5, we have total time
Step 7. Per strategy find penalty and add to cost
Step 8. Get user to incorporate weights

Doubt
How to incorporate bandwidth(MB/s)

"""
# network bandwidth
# network usage
# computeu
# SSD
# QM
# RAM

def cost_optimizer(vid, alpha, budget, **kwargs):
	'''
	video_size: 	Size of the video
	alpha:      	Relative importance of cost, wrt time 
	Comcost:    	Cost per hour of compute in dollars
	memcost:    	Cost per GB of storage per month  
	bandwidth:  	Upload Bandwidth of the user in MB/s
	bill_amount:	Amount per month for network
	FuP:        	Upload Limit in MB
	storage_time:	Intended time of storage in days
	'''
	# arg_dict = {'comcost':40, 'memcost': 400,'bandwidth':1.1 , 'bill_amount': 900*100,'FuP': 100 ,'storage_time': 90, 'quality_mode':False, 'quality_loss_thresh':0.15}
	f = open("optim.txt")
	i = f.read()
	arg_dict = json.loads(i)

	comcost = float(arg_dict['comcost'])
	memcost = float(arg_dict['memcost'])
	bandwidth = float(arg_dict['bandwidth'])
	bill_amount = float(arg_dict['bill_amount'])
	FuP = float(arg_dict['FuP'])
	storage_time = float(arg_dict['storage_time'])
	quality_mode = arg_dict['quality_mode']
	quality_loss_thresh = float(arg_dict['quality_loss_thresh'])

	# print(bandwidth)

	tes = ["1 N", "1 Y", "2 N", "2 Y", "4 N", "4 Y"]
	# Estimation of time taken to upscale per frame using that strategy
	comp_factors = [0.005, 0.01, 0.035, 0.027, 0.028, 0.024]
	# Estimation of network usage. Amount of data sent originally / Amount of data sent using that strategy
	netw_factors = [1.02, 1.96, 3.3, 3.75, 13.95, 15.3]
	# Estimation of quality loss using a particular strategy
	qual_loss_factors  = [0.01, 0.03, 0.06, 0.05, 0.14, 0.11]

	# To get frame_count, and size of video
	inp = cv2.VideoCapture(vid)
	frame_count = float(inp.get(cv2.CAP_PROP_FRAME_COUNT))
	siz = os.stat(vid).st_size

	cost_list = []
	time_list = []
	penalties = []


	cost_imp = alpha 
	time_imp = 1 - cost_imp

	for i in range(len(tes)):
		# Compute Cost: No. of frames * time per frame * cost/sec
		# Network Cost: Amount Paid per second * Transfer Time * Video Size / FuP
		mb_siz = siz / 10**6
		# print(mb_siz)
		transfer_time = mb_siz/(bandwidth * netw_factors[i])
		amount_per_second = bill_amount/(2592)
		network_cost = amount_per_second * transfer_time * (mb_siz / FuP)
		# print(f'network for strategy {tes[i]}:{network_cost}')
		compute_cost = (frame_count * comp_factors[i] * comcost)/3600 
		# print(f'compute for strategy {tes[i]}:{compute_cost}')
		storage_cost = storage_time/30 * memcost * mb_siz/(1000*netw_factors[i])
		# print(f'Storage Cost for strategy {tes[i]}:{storage_cost}')
		total_cost = network_cost + compute_cost
		# TODO: Change This
		penalty = qual_loss_factors[i] * total_cost
		penalties.append(penalty)
		# print(f'penalty for strategy {tes[i]}:{penalty}')
		consolidated_cost = total_cost + penalty
		# print(f'Consolidated Cost for strategy {tes[i]}:{consolidated_cost}')
		# print(f'Amount of data sent for {tes[i]}:{mb_siz/netw_factors[i]}')
		# Cost is given by consolidated cost
		# Time is given by total_time
		total_time = transfer_time + frame_count * comp_factors[i]
		use_time = total_time /50
		# print(f'Transfer Time for strategy {tes[i]}:{transfer_time}')
		# print(f'Total Time for strategy {tes[i]}:{total_time}')
		#cost_list.append(consolidated_cost)
		#time_list.append(use_time)
		#normalized_list = normalize(np.asarray([consolidated_cost, use_time]).reshape(1,-1)).tolist()
		# print(normalized_list)
		#final_cost = cost_imp * normalized_list[0][0] + time_imp * normalized_list[0][1]
		final_cost = cost_imp * consolidated_cost + time_imp * use_time
		# print(f'Final Cost for {tes[i]}:{final_cost}')
		if(budget != 0 and consolidated_cost>budget):
			cost_list.append(10**7)
			continue
		if(quality_loss_thresh != 0 and quality_loss_thresh<qual_loss_factors[i]):
			cost_list.append(10**7)
			continue
		cost_list.append(final_cost)
		# print('\n\n')
	'''norm_cost_list = normalize(np.asarray(cost_list).reshape(1,-1)).tolist()
	norm_time_list = normalize(np.asarray(time_list).reshape(1,-2).tolist())
	# print(norm_cost_list)
	# print(norm_time_list)
	final_list = []
	for i, j in zip(norm_cost_list[0], norm_time_list[0]):
		final_cost = cost_imp * i + time_imp * j
		# print(f'Final Cost :{final_cost}')
		final_list.append(final_cost)'''
	#strat = tes[final_list.index(min(final_list))]
	strat = tes[cost_list.index(min(cost_list))]

	if(quality_mode):
		strat = tes[penalties.index(min(penalties))]

	return strat


if __name__ == '__main__':
	# print('Video, alpha, Compute Cost per hour, Storage cost per month, Bandwidth of user, Bill Amount of network, FuP of user, Storage time intended')
	best_strat = cost_optimizer(sys.argv[1], float(sys.argv[2]), comcost=100, budget = 15, quality_mode=False)
	print(f'BEST STRATEGY: {best_strat}')
	os.system("python client.py " + sys.argv[1] + " " + best_strat)