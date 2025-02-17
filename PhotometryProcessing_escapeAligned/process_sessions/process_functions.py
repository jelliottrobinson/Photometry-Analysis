# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 15:43:05 2021

@author: FISXV1
"""
import numpy as np
import matplotlib.pyplot as plt
# imports that may be used here
# the following line must be replaced with a relative path in place of the
# absolute path - otherwise, this will only work while the project is stored in
# austen's folder in the Z drive

# use the following to handle imports explicitly
from pre_process.process_params import (EXPERIMENT_NAME, Y_LIM, X_LIM, 
                                        EPOCH_ONSET, PEAK_START_TIME, 
                                        PEAK_STOP_TIME, AUC_THRESH_FOR,
                                        AUC_THRESH_BACK)
# using * import to bring over constants, consider replacing with explicit 
# imports to remove warnings


#%% Sorting functions
# take input of arbitrary number of lists of 1D numpy arrays and unpack into
# 2D array
def epoch_unpack(*args):
    '''
    Parameters
    ----------
    *args : any number of lists of 1D numpy arrays

    Returns
    -------
    output_array: 2D numpy array composed of v-stacked input arrays

    '''
    output_array = np.empty((len(args)*len(args[0]), args[0][0].shape))
    for row in range(len(output_array)):
        output_array[row] = args[0][0]

    return(output_array)

def sort_by_ordered_stim(data):
    '''
      This function sorts filtered signal and isos data in the case that stim
    presentations are sorted by a known order.
    '''
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

    return(condition_matched_arrays, condition_matched_isos)

def sort_by_pulse_width(data):
    '''
      This function sorts filtered signal and isos data in the case that stim
    presentations are sorted by their corresponding ttl pulse width.  
    '''        
    stims = list(data.exp_dict[1].values())
    condition_matched_arrays = dict()
    condition_matched_isos = dict()
    
    for stim in stims:
        condition_matched_arrays.setdefault(stim)
        condition_matched_isos.setdefault(stim)
    for pulse_width in data.exp_dict[1].keys():
        temp_arrays = []
        temp_isos = []
        for ttl_data_pair in data.epoch_dict:
            if ttl_data_pair[0] == pulse_width:
                temp_arrays.append(ttl_data_pair[1])
                temp_isos.append(ttl_data_pair[2])
        condition_matched_arrays[data.exp_dict[1][pulse_width]] = (temp_arrays)
        condition_matched_isos[data.exp_dict[1][pulse_width]] = (temp_isos)
        
    return(condition_matched_arrays, condition_matched_isos)   

def sort_by_one_stim(data):
    '''
      This function prompts the user for an input to use as the name to the 
    experimental stimulus in the case that only a single stimulus was used in
    the experiment and then formats the data in a similar manner to the other
    conditions.
    '''
    stim = data.exp_dict[1]
    condition_matched_arrays = dict(zip([stim], [data.sig_filtered]))
    condition_matched_isos = dict(zip([stim], [data.isos_filtered]))
    
    return(condition_matched_arrays, condition_matched_isos)

def downsample(data, N):
    '''
      This function takes a numpy array (data) as input and downsamples by 
    rate(N). The output is the downsampled numpy array.
    '''
    temp_lst = list(data)
    data_ds = []
    for i3 in range(0, len(temp_lst), N):
        data_ds.append(np.mean(temp_lst[i3:i3+N-1]))
    
    return(data_ds)

#%% Plotting functions
# possible way to handle plotting if needed
def epoch_plot(data, error, time, stim, total_sessions, total_trials,
               return_subplot = False):
    fig = plt.figure(figsize=(20, 35))
    ax0 = fig.add_subplot(311)
    x_axis = time
    y_axis = data
    p1, = ax0.plot(x_axis, y_axis, linewidth=2, color='black', label='dLight')
    p2 = ax0.fill_between(x_axis, data+error, data-error, 
                          facecolor='green', alpha=0.2)
    if EPOCH_ONSET:
        p3 = ax0.axvline(x=0, linewidth=3, color='slategray', label='Stim Onset')
        for x in range(4):
            p4 = ax0.axvline(x=1+x, linewidth=3, color='slategray')

    ax0.set_ylabel('Z-Score')
    ax0.set_xlabel('Seconds')
    ax0.set_xlim(X_LIM[0], X_LIM[1])
    ax0.set_ylim(Y_LIM[0], Y_LIM[1])
    if EPOCH_ONSET:
        ax0.legend(handles=[p1, p3, p4], loc='upper right')
    if EXPERIMENT_NAME:
        ax0.set_title(f'{EXPERIMENT_NAME}: {stim}, n={total_sessions} '
                      f'({total_trials} Trials per Session)')    
    else:
        ax0.set_title(f'{stim}, n={total_sessions} '
                      f'({total_trials} Trials per Session)')   
    if return_subplot:
        return(fig, ax0)
    else:
        return(fig)

def add_hm(fig, TRANGE, data, size, color_lim, time_lim):
    ax1 = fig.add_subplot(size)
    hm_data = data.copy()
    hm_data.reverse()
    pt_per_sec = len(hm_data[0])/TRANGE[1] #consider replacing TRANGE
    hm_start = time_lim[0]
    hm_end = time_lim[1]
    temp_list = []
    for i in range(0, len(hm_data)):
        temp_list.append(hm_data[i][round((abs(TRANGE[0])+hm_start)*pt_per_sec):
                                 round((abs(TRANGE[0])+hm_end)*pt_per_sec)])
        hm_data[i] = temp_list[i] 
    cs = ax1.imshow(hm_data, cmap=plt.cm.plasma, interpolation='none', 
                    aspect="auto", vmin = color_lim[0], 
                    vmax = color_lim[1], 
                    extent=[hm_start, hm_end, 0,  len(hm_data)])
    cbar = fig.colorbar(cs, pad=0.01, fraction=0.02)
    ax1.set_title('Average Trial Z-Score (Stim Onset)')
    ax1.set_ylabel('Trials')
    ax1.set_xlabel('Seconds from Stimulus Onset')
    return(fig)

def add_mouse_hm(fig, TRANGE, data, size, color_lim, time_lim):
    ax1 = fig.add_subplot(size)
    hm_data = data.copy()
    hm_data.reverse()
    pt_per_sec = len(hm_data[0])/TRANGE[1] #consider replacing TRANGE
    hm_start = time_lim[0]
    hm_end = time_lim[1]
    temp_list = []
    for i in range(0, len(hm_data)):
        temp_list.append(hm_data[i][round((abs(TRANGE[0])+hm_start)*pt_per_sec):
                                 round((abs(TRANGE[0])+hm_end)*pt_per_sec)])
        hm_data[i] = temp_list[i] 
    cs = ax1.imshow(hm_data, cmap=plt.cm.plasma, interpolation='none', 
                    aspect="auto", vmin = color_lim[0], 
                    vmax = color_lim[1], 
                    extent=[hm_start, hm_end, 0,  len(hm_data)])
    cbar = fig.colorbar(cs, pad=0.01, fraction=0.02)
    ax1.set_title('Average Trial Z-Score (Stim Onset)')
    ax1.set_ylabel('Mouse')
    ax1.set_xlabel('Seconds from Stimulus Onset')
    return(fig)

#%% Epoch stats functions

# =============================================================================
# def time_arr(data, epoch_start = TRANGE[0], epoch_stop = TRANGE[1]+TRANGE[0]):
#     steps = len(data)
#     time = np.linspace(epoch_start, epoch_stop, steps)
#     
#     return(time)
# 
# def peak_between(data, start_time = PEAK_START_TIME, 
#                  stop_time = PEAK_STOP_TIME, time_arr_start = TRANGE[0],
#                  time_arr_stop = TRANGE[1]+TRANGE[0]):
#     
#     time = time_arr(data, epoch_start = time_arr_start, epoch_stop = 
#                     time_arr_stop)
#     inds = np.where((time>=start_time) & (time<=stop_time))
#     inds
#     peak = max(data[inds[0][0]:inds[0][-1]])
#     return(peak)    
# 
# def peak_delay(data, start = PEAK_START_TIME, stop = PEAK_STOP_TIME, 
#                time_arr_start = TRANGE[0], 
#                time_arr_stop = TRANGE[1]+TRANGE[0]):
#     time = time_arr(data, epoch_start = time_arr_start, epoch_stop = 
#                     time_arr_stop)
#     time_start = time_arr_start
#     time_stop = time_arr_stop
#     # the following will pick the first instance of the peak value in the 
#     # data array. If selecting for a peak value that occurs multiple time, the 
#     # fuction may choose an incorrect time value
#     peak_ind = np.where(data == peak_between(data, start_time = start, 
#                                              stop_time = stop, 
#                                              time_arr_start = time_start,
#                                              time_arr_stop = time_stop))
#     peak_delay = time[peak_ind]
#     
#     return(peak_delay)
# 
# def get_fwhm(data, time_arr_start = TRANGE[0], 
#              time_arr_stop = TRANGE[1]+TRANGE[0]): #This function works when the Z-score of the stimulus spike is greater than 2x the largest noisy spike
#     time = time_arr(data, epoch_start = time_arr_start, 
#                     epoch_stop = time_arr_stop)
#     half_max = peak_between(data)/2
#     peak_ind = np.where(data == peak_between(data))
#     forward_ind = backward_ind = peak_ind[0][0]
#     while data[forward_ind+1]>=half_max and forward_ind+1<len(data)-1:
#         forward_ind +=1
#     while data[backward_ind-1]>=half_max:
#         backward_ind -= 1
#     half_max_inds = [backward_ind, forward_ind]
#     half_max_times = (time[backward_ind], time[forward_ind])
#     fwhm = half_max_times[-1] - half_max_times[0] #full width at half max
#     
#     return(fwhm, half_max_inds)
# 
# def get_auc(data, time_arr_start = TRANGE[0], 
#             time_arr_stop = TRANGE[1]+TRANGE[0]):
#     time = time_arr(data, epoch_start = time_arr_start, 
#                     epoch_stop = time_arr_stop)
#     peak_ind = np.where(data == peak_between(data))
#     forward_ind = backward_ind = peak_ind[0][0] #grab the single integer value (stored in a np.array in a tuple; reason for the double indexing)
#     while ((data[forward_ind]>data[forward_ind+1] or data[forward_ind]>AUC_THRESHOLD) and 
#            data[forward_ind+1]>=0): #Iterates forward from peak value checking that the curve is decreasing but also above 0
#         forward_ind += 1
#     while data[backward_ind]>data[backward_ind-1] and data[backward_ind-1]>=0:
#         backward_ind -= 1
#     print(f'AUC calculation starts at t={time[backward_ind]}s')
#     print(f'AUC calculation stops at t={time[forward_ind]}s')
#     
#     step_size = (time[-1]-time[0])/len(time)
#     peak_slice = data[backward_ind:forward_ind]    
#     auc = np.trapz(peak_slice, dx=step_size)
#     
#     return(auc, backward_ind, forward_ind)
# =============================================================================

#%% replace TRANGE

def time_arr(data, TRANGE):
    epoch_start = TRANGE[0]
    epoch_stop = TRANGE[1]+TRANGE[0]
    steps = len(data)
    time = np.linspace(epoch_start, epoch_stop, steps)
    
    return(time)

def peak_between(data, TRANGE, start_time = PEAK_START_TIME, 
                 stop_time = PEAK_STOP_TIME):
    time = time_arr(data, TRANGE)
    inds = np.where((time>=start_time) & (time<=stop_time))
    inds
    peak = max(data[inds[0][0]:inds[0][-1]])
    return(peak)    

def peak_delay(data, TRANGE, start = PEAK_START_TIME, stop = PEAK_STOP_TIME):
    time = time_arr(data, TRANGE)
    # the following will pick the first instance of the peak value in the 
    # data array. If selecting for a peak value that occurs multiple time, the 
    # fuction may choose an incorrect time value
    peak_ind = np.where(data == peak_between(data, TRANGE, start_time = start, 
                                             stop_time = stop))
    peak_delay = time[peak_ind]
    
    return(peak_delay)

def get_fwhm(data, TRANGE): #This function works when the Z-score of the stimulus spike is greater than 2x the largest noisy spike
    time = time_arr(data, TRANGE)
    half_max = peak_between(data, TRANGE)/2
    peak_ind = np.where(data == peak_between(data, TRANGE))
    forward_ind = backward_ind = peak_ind[0][0]
    while data[forward_ind+1]>=half_max and forward_ind+1<len(data)-1:
        forward_ind +=1
    while data[backward_ind-1]>=half_max:
        backward_ind -= 1
    half_max_inds = [backward_ind, forward_ind]
    half_max_times = (time[backward_ind], time[forward_ind])
    fwhm = half_max_times[-1] - half_max_times[0] #full width at half max
    
    return(fwhm, half_max_inds)

def get_auc(data, TRANGE):
    time = time_arr(data, TRANGE)
    peak_ind = np.where(data == peak_between(data, TRANGE))
    forward_ind = backward_ind = peak_ind[0][0] #grab the single integer value (stored in a np.array in a tuple; reason for the double indexing)
    while ((data[forward_ind]>data[forward_ind+1] 
            or data[forward_ind]>AUC_THRESH_FOR) 
            and data[forward_ind+1]>=0): #Iterates forward from peak value checking that the curve is decreasing but also above 0
        forward_ind += 1
    while ((data[backward_ind]>data[backward_ind-1] 
            or data[backward_ind]>AUC_THRESH_BACK)
            and data[backward_ind-1]>=0):
        backward_ind -= 1
    print(f'AUC calculation starts at t={time[backward_ind]}s')
    print(f'AUC calculation stops at t={time[forward_ind]}s')
    
    step_size = (time[-1]-time[0])/len(time)
    peak_slice = data[backward_ind:forward_ind]    
    auc = np.trapz(peak_slice, dx=step_size)
    
    return(auc, backward_ind, forward_ind)

#%% Deprecated functions

# Choosing the sorting method is currently handled another way
# =============================================================================
# def sort(data):
#     '''
#       This function sorts the data using one of the three following functions:
#     sort_by_ordered_stim, sort_by_pulse_width, or sort_by_one_stim.
#     
#     The sorting method is decided based on the MyTDT.ttl_key_type attribute
#     
#     Parameters
#     ----------
#     data : Input data object of MyTDT type
# 
#     Returns
#     -------
#     signal_dict: dictionary where the keys are a string stating
#       the type of experimental stimulus and the values are list of epoch
#       filtered arrays.
#         
#     isos_dict: same as previouse, but the epoch filtered arrays 
#       are the isos signal instead of the measured signal.
# 
#     '''
#     if data.ttl_key_type == 'single stimulus':
#         signal_dict, isos_dict = sort_by_one_stim(data)
#     elif data.ttl_key_type == 'ttl pulse width':
#         signal_dict, isos_dict = sort_by_pulse_width(data)
#     elif data.ttl_key_type == 'presentation order':
#         signal_dict, isos_dict = sort_by_ordered_stim(data)
#     else:
#         print('data.ttl_key_type attribute is not recognized')
#         
#     return(signal_dict, isos_dict)
# =============================================================================

# epoch size match with the following code, this appears unnecessary because
# the arrays are constructed in a way the assures they are all the same size
# convert to a function if ever used
# =============================================================================
# arr_lens = []
# for dct in sig_epoch_struct:
#     for lst in list(dct.values()):
#         for arr in lst:
#             arr_lens.append(len(arr))
#             
# arr2_lens= []
# for dct in isos_epoch_struct:
#     for lst in list(dct.values()):
#         for arr in lst:
#             arr2_lens.append(len(arr))
# =============================================================================