# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 10:42:05 2022

@author: FISXV1
"""

#%% Imports - remove unneeded ones
import numpy as np
import tdt
import os
import pickle 
from my_tdt_obj import MyTDT
from auto_populate import one_time_inputs
#%% Load TDT runs for combining
file1_path = r'Z:\PhotometryData\Tone\4Tones\TDT_raw_2parts\151-1N-220202-4Tones.Part1'
file2_path = r'Z:\PhotometryData\Tone\4Tones\TDT_raw_2parts\151-1N-220202-4Tones.Part2'

process_output_path = r'Z:\PhotometryData\Tone\4Tones\pre_processed'

tdt1 = tdt.read_block(file1_path)
tdt2 = tdt.read_block(file2_path)

key, exp_in = one_time_inputs()
mytdt1 = MyTDT(tdt1, ttl_key_type = key, exp_input = exp_in)
mytdt2 = MyTDT(tdt2, ttl_key_type = key, exp_input = exp_in)

#%% Combine TDT runs

# epoch_dict updated
for item in mytdt2.epoch_dict:
    mytdt1.epoch_dict.append(item)

# epoch_inds updated    
size = len(mytdt1.time)
for ind in mytdt2.epoch_inds:
    mytdt1.epoch_inds.append(ind + size)

# epoch_onset and offset updated
temp_onset = list(mytdt1.epoch_onset)
temp_offset = list(mytdt1.epoch_offset)
for onset in list(mytdt2.epoch_onset):
    temp_onset.append(onset + mytdt1.time[1] + mytdt1.time[size-1])
for offset in list(mytdt2.epoch_offset):
    temp_offset.append(offset + mytdt1.time[1] + mytdt1.time[size-1])
mytdt1.epoch_onset = np.array(temp_onset)
mytdt1.epoch_offset = np.array(temp_offset)
        
# time updated
temp_time = list(mytdt1.time)    
for t in list(mytdt2.time):
    temp_time.append(t + mytdt1.time[1] + mytdt1.time[size-1])
mytdt1.time = np.array(temp_time)

# isos and sig updated
mytdt1.isos = np.append(mytdt1.isos, mytdt2.isos)
mytdt1.sig = np.append(mytdt1.sig, mytdt2.sig)

# filtered isos and sig updated
for sig in mytdt2.sig_filtered:
    mytdt1.sig_filtered.append(sig)
for isos in mytdt2.isos_filtered:
    mytdt1.isos_filtered.append(isos)
    
# stim keys updated
for key in mytdt2.stim_keys:
    mytdt1.stim_keys.append(key)
    
# total epochs updated
mytdt1.total_epochs = mytdt1.total_epochs + mytdt2.total_epochs

#%% Add custom code here for speicific use cases - comment out all code in this
# section if you didn't write it yourself for the use case

mytdt1.epoch_dict[12] = (0.005, mytdt1.epoch_dict[12][1], mytdt1.epoch_dict[12][2])
mytdt1.experiment = 'four_tone'
mytdt1.stim_keys[12] = 0.005
mytdt1.exp_dict = mytdt2.exp_dict

#%% Save the combined and preprocessed run

if __name__ == '__main__':
    file_name = file1_path.split('\\')[-1]
    with open(f'{process_output_path}\\{file_name}.bin','wb') as f:
         pickle.dump(mytdt1, f)

