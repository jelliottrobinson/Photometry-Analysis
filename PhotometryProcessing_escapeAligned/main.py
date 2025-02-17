# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 11:35:06 2021

@author: FISXV1
"""
#%% import packages
import numpy as np
import os
import sys
import pickle
import math
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
import pandas as pd
import gc
# internal imports
sys.path.append('.\\pre_process')
sys.path.append('.\\process_sessions')
from my_tdt_obj import MyTDT
import my_tdt_obj
from process_functions import (epoch_unpack, sort_by_ordered_stim, 
                               sort_by_pulse_width, sort_by_one_stim,
                               epoch_plot, add_hm, downsample, time_arr,
                               peak_between, peak_delay, get_fwhm, get_auc,
                               add_mouse_hm)

from process_params import (BASELINE_PER, DOWNSAMPLE_RATE, 
                            EXPERIMENT_NAME, Y_LIM, X_LIM, EPOCH_ONSET,
                            EPOCH_AVG_HM, HM_COLOR_LIM, HM_TIME_LIM,
                            EPOCH_AVG_HM2, HM_COLOR_LIM2, HM_TIME_LIM2,
                            RAW_MV_STREAM, RAW_MV_START, FIG_SAVE, EPOCH_STATS,
                            MAIN_INPUT, MAIN_OUTPUT, EPOCH_MOUSE_HM,
                            MOUSE_HM_COLOR_LIM, MOUSE_HM_TIME_LIM,
                            PEAK_START_TIME, PEAK_STOP_TIME)

#%% Define input and output paths
# These are pulled from user defined variables in process_params
raw_data_path = MAIN_INPUT
output_path = MAIN_OUTPUT
folder = os.listdir(raw_data_path)

#%% Begin processing conditionally based on the input data type
print('loading data...')
files = []
for file_path in folder:
    with open(f'{raw_data_path}\\{file_path}','rb') as f:
         file = pickle.load(f)
    files.append(file)
    
ttl_types = []
for file in files:
    ttl_types.append(file.ttl_key_type)
    
sig_epoch_struct = []
isos_epoch_struct = []   

if all([ttl == 'presentation order' for ttl in ttl_types]):
    for file in files:
        temp_sig, temp_isos = sort_by_ordered_stim(file)
        sig_epoch_struct.append(temp_sig)
        isos_epoch_struct.append(temp_isos)   
elif all([ttl == 'single stimulus' for ttl in ttl_types]):
    for file in files:
        temp_sig, temp_isos = sort_by_one_stim(file)
        sig_epoch_struct.append(temp_sig)
        isos_epoch_struct.append(temp_isos)        
elif all([ttl == 'ttl pulse width' for ttl in ttl_types]):
    for file in files:
        temp_sig, temp_isos = sort_by_pulse_width(file)
        sig_epoch_struct.append(temp_sig)
        isos_epoch_struct.append(temp_isos)    
else:
    print('Ttl types do not match. Rerun this script with a data set '
          'that only contains files of the same experiment type.')
print('data loaded')    

TRANGE = files[0].epoch_trange
    
#%% Format data into simple np.arrays for processing

# create dictionary where the keys are the various experimental condtions and 
# paired values are 2D arrays created from the various epoch arrays of the same
# experimental condition
# for sig, isos in zip(sig_epoch_struct, isos_epoch_struct):

N = int(DOWNSAMPLE_RATE) #downsampling rate - only change this from the
if type(DOWNSAMPLE_RATE) == float:
    print('Downsampling rate converted to interger.')
# process_params.py file in the pre_process folder
if N > 1:
    for i in range(len(sig_epoch_struct)):
        dct = sig_epoch_struct[i]
        for key in dct:
            lst = dct[key]
            for i2 in range(len(lst)):
                small_lst = downsample(lst[i2], N)
                sig_epoch_struct[i][key][i2] = small_lst
    # downsample isosbestic
    for i in range(len(isos_epoch_struct)):
        dct = isos_epoch_struct[i]
        for key in dct:
            lst = dct[key]
            for i2 in range(len(lst)):
                small_lst = downsample(lst[i2], N)               
                isos_epoch_struct[i][key][i2] = small_lst
else:
    pass

# create the epoch time array
time_size = len(small_lst)
ts1 = np.linspace(TRANGE[0], TRANGE[1]+TRANGE[0], time_size)

# set up a simple data structure: stim_dict
# this dictionary uses the experimental stimuli as keys and stores a list of 
# lists that each contain a signal array paired with its' isos array
stim_dict = {}
for stim in sig_epoch_struct[0]:
    stim_dict.setdefault(stim)
    stim_dict[stim] = []
    
# populate the stim_dict array
sessions = len(sig_epoch_struct)
stims = list(sig_epoch_struct[0].keys())
trials = len(sig_epoch_struct[0][stims[0]])
if trials < len(sig_epoch_struct[0][stims[0]]):
    print('\n\nNumber of trials was modified from the first sample. Correct '
          'this value if unintended\n\n')
for session in range(sessions):
    for stim in stims:
        for trial in range(trials):
            stim_dict[stim].append([sig_epoch_struct[session][stim][trial], 
                                    isos_epoch_struct[session][stim][trial]])

# Generate fit lines for sig vs. isos to calculate delta F
fit_lines = []
signal_df = []
atz_stims = []
for stim in stims:
    for y, x in stim_dict[stim]: # isos must be the x variable
        bls = np.polyfit(x, y, 1)
        fit_line = np.multiply(bls[0], x) + bls[1]
        fit_lines.append(fit_line)
        signal_df.append(y-fit_line)    
        atz_stims.append(stim)
        
all_trial_z = []
total_std = 0
count = 0

# normal method for sampling baseline period  
for trial in signal_df:
    ind = np.where((np.array(ts1)<BASELINE_PER[1]) & 
                   (np.array(ts1)>BASELINE_PER[0]))
    temp_mean = np.mean(trial[ind])
    temp_std = np.std(trial[ind])
    total_std += temp_std
    count += 1
    all_trial_z.append((trial-temp_mean)/temp_std)

print(f'\nAverage Standard Deviation = {total_std / count}\n')    
    
all_session_z = []
all_session_error = []
asz_stims = []

for stim in range(len(stims)):
    for session in range(sessions):
        asz_stims.append(stims[stim])
        temp_array = np.zeros((len(all_trial_z[0]), trials))
        for trial in range(0, trials):
            temp_array[:, trial] = all_trial_z[trial+(trials*session)+
                                               (trials*sessions*stim)]        
        all_session_z.append(np.mean(temp_array, axis = 1))
        all_session_error.append(np.std(temp_array, axis = 1)
                                 /math.sqrt(trials))
       
# get the average z-score for all sessions combined and calculate 
# the standard error
final_z = []
final_error = []
for stim in range(len(stims)):
    temp_array = np.empty((len(all_session_z[0]), sessions))
    for session in range(sessions):
        temp_array[:, session] = all_session_z[session+(stim*sessions)]
    final_z.append(np.mean(temp_array, axis=1))
    final_error.append(np.std(temp_array, axis=1)/
                       math.sqrt(np.size(temp_array, axis=1)))

# get the average z-score for each trial for heatmapping
avg_trial_z = []
for stim in range(len(stims)):
    temp_avg_trial_z = []
    for trial in range(0, trials):
        temp_array = np.empty((len(all_trial_z[0]), sessions))
        for session in range(0, sessions):
            temp_array[:, session] = all_trial_z[trial+(session*trials)+
                                                 (trials*sessions*stim)]
        temp_avg_trial_z.append(np.mean(temp_array, axis = 1))   
    avg_trial_z.append(temp_avg_trial_z)

'''
Main products of the data processing step:
    
final_z: averaged and z-scored epoch stream of signal channel
final_error: error values of the final_z stream - use to make std error bars

sessions: number of sessions processed
stims: list of stimuli in the input data
trials: number of trials within each session

stim_dict: dictionary that pairs stimulus keys with corresponding data
    signal and isos data are coupled in order of how they a loaded from the 
    input folder - data is downsampled by DOWNSAMPLE_RATE
'''

#------------------------------------------------------------------------------
# Use the following as the default plotting method
plot_list = []
for i in range(len(stims)):
    fig0, ax0 = epoch_plot(final_z[i], final_error[i], ts1, stims[i], sessions,
                     trials, return_subplot = True)
    if EPOCH_AVG_HM:
        fig0 = add_hm(fig0, TRANGE, avg_trial_z[i], 312, 
                      HM_COLOR_LIM, HM_TIME_LIM)
        
    if EPOCH_MOUSE_HM:
        
        session_dict = {}
        search_window = np.where((ts1>PEAK_START_TIME) & 
                                 (ts1 < PEAK_STOP_TIME))
        for z in all_session_z:
            search_array = z[search_window]
            search_max = np.max(search_array)
            session_dict[search_max] = z
        session_dict_sorted = dict(sorted(session_dict.items()))
        session_list_sorted = list(session_dict_sorted.values())
        x = session_list_sorted
        
# Flip two rows in heatmap        
# =============================================================================
#         x[14], x[15] = x[15], x[14]
# =============================================================================
        
        fig0 = add_mouse_hm(fig0, TRANGE, x, 312, 
                      MOUSE_HM_COLOR_LIM, MOUSE_HM_TIME_LIM)    
        
    if EPOCH_AVG_HM2:
        fig0 = add_hm(fig0, TRANGE, avg_trial_z[i], 313, 
                      HM_COLOR_LIM2, HM_TIME_LIM2)
        
    if FIG_SAVE:
        fig0.savefig(f'{output_path}\\{stims[i]}.pdf', format='pdf')  
    
# add individual dLight traces in the background
# =============================================================================
# for z in all_session_z:
#     ax0.plot(ts1, z, color = 'lightgray', zorder = 1)
# =============================================================================
#------------------------------------------------------------------------------

#%% Produce raw data streams (mV)

# load in the raw data
if RAW_MV_STREAM:
    for file in files: 
        raw_sig = file.sig
        raw_isos = file.isos
        fs_time = file.time
        
        # cut off the first second to remove LED-ON artifiact
        start_time = RAW_MV_START
        start_ind = np.where(fs_time>=start_time)
        raw_sig = raw_sig[start_ind]
        raw_isos = raw_isos[start_ind]
        fs_time = fs_time[start_ind]
        
        fig1 = plt.figure(figsize=(20, 35))
        ax1 = fig1.add_subplot(311)
        
        p1, = ax1.plot(fs_time, raw_sig, linewidth=2, color='green', 
                       label='Signal')
        p2, = ax1.plot(fs_time, raw_isos, linewidth=2, color='blue', 
                       label='Isos')
        
        ax1.set_ylabel('mV')
        ax1.set_xlabel('Seconds')
        ax1.legend(handles=[p1, p2], loc='upper right')
        ax1.set_title(f'Raw Stream: {file.info.blockname}')   
    
#%% Produce epoch stats for each mouse individually

#stats_frames = []
if EPOCH_STATS:
    epoch_stats = {}
    for stim_ind in range(len(stims)):
        stim = stims[stim_ind]
        epoch_stats.setdefault(stim)    
        peak_dict = {}
        delay_dict = {}
        fwhm_dict = {}
        auc_dict = {}
        
        for mouse_ind in range(len(files)):
            # create dictionaries
            split_name = files[mouse_ind].info.blockname.split('-')
            if len(split_name[1]) == 2:
                mouse = f'{split_name[0]}-{split_name[1]}'
            else:
                mouse = split_name[0]
            
            peak_dict.setdefault(mouse)
            delay_dict.setdefault(mouse)
            fwhm_dict.setdefault(mouse)
            auc_dict.setdefault(mouse)
            # produce epoch stats for given mouse and stimulus
            data = all_session_z[stim_ind*len(files) + mouse_ind]
            stat_time = time_arr(data, TRANGE)
            peak = peak_between(data, TRANGE)
            peak_time = peak_delay(data, TRANGE)[0]
            fwhm, fwhm_inds = get_fwhm(data, TRANGE)
            auc, peak_start_ind, peak_stop_ind = get_auc(data, TRANGE)
            
            fig3 = plt.figure(figsize=(20, 35))
            ax3 = fig3.add_subplot(311)
            
            p1, = ax3.plot(stat_time, data, linewidth=1, color='black', 
                           label='dLight') #line graph
            p2 = (ax3.fill_between(stat_time[peak_start_ind:peak_stop_ind], 
                                   data[peak_start_ind:peak_stop_ind], 
                                   np.zeros(peak_stop_ind-peak_start_ind), 
                                   facecolor='blue', alpha=0.2))
            p3 = (ax3.plot(stat_time[fwhm_inds], np.ones(np.size(fwhm_inds))*
                           (peak_between(data, TRANGE)/2), linewidth = 2, 
                           color='red'))
            p4 = ax3.axvline(x=0, linewidth=3, color='slategray', 
                             label='Stim Onset')
            p5 = ax3.axhline(y=0, linewidth=1, color='slategray')
            p6 = ax3.plot(peak_time, peak, marker = 'v', color = 'black')
            
            ax3.set_ylabel('z-Score')
            ax3.set_xlabel('Seconds')
            ax3.set_xlim(X_LIM[0], X_LIM[1]) #user must adjust the min and max values to determine the range they want to see the bottom graph
            #ax0.set_ylim(-1, math.ceil(max_zscore)+1)
            ax3.set_ylim(Y_LIM[0], Y_LIM[1])
            #ax0.legend(handles=[p1, p3], loc='upper right')
            ax3.set_title(f'{mouse}: Epoch Average with AUC and FWHM')
            
            # populate dictionaries with data
            peak_dict[mouse] = peak
            delay_dict[mouse] = peak_time
            fwhm_dict[mouse] = fwhm
            auc_dict[mouse] = auc
            #stats_frames.append(pd.DataFrame())
            
        # created pandas Series and DataFrames
        peak_series = pd.Series(peak_dict)
        delay_series = pd.Series(delay_dict)
        fwhm_series = pd.Series(fwhm_dict)
        auc_series = pd.Series(auc_dict)
        stats_frame = pd.DataFrame({'Peak': peak_series, 'Peak Delay':
                                    delay_series, 'fwhm': fwhm_series, 
                                    'auc' : auc_series})
        epoch_stats[stim] = stats_frame   


