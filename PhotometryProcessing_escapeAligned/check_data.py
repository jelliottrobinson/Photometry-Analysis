# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 13:00:09 2022

@author: FISXV1
"""
import sys
sys.path.append('.\\pre_process')
sys.path.append('.\\process_sessions')
import pickle
import my_tdt_obj
from my_tdt_obj import MyTDT
import numpy as np

file_path = r'Z:\Austen\striatumHeterogeneityProject\Photometry\GFP_LoomExperiments\InvertedReceding_Looms\pre_processed'
file_name = r'1108L-240603-invertedRecedingLoom.bin'


with open(f'{file_path}\\{file_name}','rb') as f:
     file = pickle.load(f)

#%% change epoch_trange

# =============================================================================
# file.epoch_trange = [-10, 21]
# =============================================================================

#%% Save the loaded file to output_path
# =============================================================================
# temp = list(file.epoch_dict[6])
# temp[0] = np.float64(0.001)
# file.epoch_dict[6] = tuple(temp)
# file.info.blockname = r'OPN4.D1.N-230714-ReCyGrUV_0.001uW.bin'
# output_path = r'Z:\Sofia\For Austen to Troubleshoot\pre_processed'
# 
# with open(f'{output_path}\\{file_name}','wb') as f:
#      pickle.dump(file, f)
# =============================================================================

