# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 16:16:04 2022

@author: auste
"""

import numpy as np
import os
import sys
import pickle
# internal imports
sys.path.append('./pre_process')
sys.path.append('./process_sessions')
from my_tdt_obj import MyTDT
#%% load MyTDT files, last loaded is 'data'

raw_data_path = (r'C:/Users/auste/Documents/Python/PythonProjects/PhotometryProcessing/pre_process/test_inputs/MyTDT_objects/Ordered_LongerFade_Batch')
folder = os.listdir(raw_data_path)

files = []
for file_path in folder:
    with open(f'{raw_data_path}\\{file_path}','rb') as f:
         data = pickle.load(f)
    files.append(data)

#%% actual function

# =============================================================================
# stims = list(data.exp_dict[1].values())
# condition_matched_arrays = dict()
# condition_matched_isos = dict()
# 
# for stim in stims:
#     condition_matched_arrays.setdefault(stim)
#     condition_matched_isos.setdefault(stim)
# for pulse_width in data.exp_dict[1].keys():
#     temp_arrays = []
#     temp_isos = []
#     for ttl_data_pair in data.epoch_dict:
#         if ttl_data_pair[0] == pulse_width:
#             temp_arrays.append(ttl_data_pair[1])
#             temp_isos.append(ttl_data_pair[2])
#     condition_matched_arrays[data.exp_dict[1][pulse_width]] = (
#         temp_arrays)
#     condition_matched_isos[data.exp_dict[1][pulse_width]] = (
#         temp_isos)
# =============================================================================

stims = []
condition_arrays = []
condition_isos = []
for condition in data.exp_dict.items():
    stims.append(condition[0])
    temp_array = []
    temp_isos = []
    for order in condition[1]:
       temp_array.append(data.sig_filtered[order])
       temp_isos.append(data.isos_filtered[order])
    condition_arrays.append(temp_array)
    condition_isos.append(temp_isos)
condition_matched_arrays = dict(zip(stims, condition_arrays))
condition_matched_isos = dict(zip(stims, condition_isos))