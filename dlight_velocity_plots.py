# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:35:02 2024

@author: FISXV1
"""
import os
import csv
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks


cohort1_folder_name = r''
cohort2_folder_name = r''
output_path = r''
vline = 0

# CHECK ORDER OF THE FOLLOWING

# populate cohort order lists with strings of names of mice in the order
# that matches the order of delays provided in the cohort delays lists
cohort1_order = ['951-1N', '955-1N', '955-1R', '955-1L', '956-1N', '956-1R', '958-1N', '958-1R']
cohort2_order = ['1064-1N', '1114R', '1125-1N']

# populate cohort delays lists with time between stimulus onset and time of
# escape. Populate with list of zeros if aligning to time of stimulus onset
cohort1_delays = [6.3, 2.4, 5.2, 1.35, 3.55, 6.2, 3.5, 3.5]
cohort2_delays = [1.5, 4.15, 6.9]

plot_dict = {}
for index in range(len(folder)):
    mouse_name = folder[index]
    mouse_name_list = mouse_name.split('-')
    if len(mouse_name_list[1]) == 2:
        mouse_name = f'{mouse_name_list[0]}-{mouse_name_list[1]}'
    else:
        mouse_name = mouse_name_list[0]
    
    plot_dict[mouse_name] = [all_session_z[index]]
     
    
def get_velocity_array_cohort1(path):
    filename = ''
    loom_index = int(0)
    stop_index = int(0)
    total_time = float(0)
    loom_start = 0
    frames = int(0)
    fs = float(0) 
    time_array = []
    xposition_array = []
    distance_from_shelter = []
    xvelocity_array = []
    peak_indices = []
    peak_times = []
    animal_id = ''
    loom_type = ''
    polyfit_function = None
    max_velocity_time = float(0)
    max_velocity = float(0)
    
    filename = path

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        
        
        current_line = []
        header_count = 0
        
        current_line = next(csv_reader)
        header_count = int(current_line[1])
        
        # iterate through csv until the "Animal Number" line is found
        for line in csv_reader:
            if line[0] == "Loom":
                loom_type = line[1]
            if line[0] == "Animal Number":
                animal_id = line[1]
                break
        
        # burn empty line in csv file
        next(file)
            
        df = pd.read_csv(file)
        
    fs = float(df['Trial time'][2])

    loom_index += 1
    for value in df[f'{loom_type} Loom']:
        if math.isnan(value):
            pass
        elif value == 0:
            loom_index += 1
        else:
            break

    total_time = 10
    frames = int(total_time/fs)
    stop_index = loom_index + frames

    time_array = list(df['Trial time'][loom_index:stop_index])
    xposition_array = list(df['X center'][loom_index:stop_index])


    # convert stings to floats
    for index in range(len(time_array)):
        time_array[index] = float(time_array[index])
        xposition_array[index] = float(xposition_array[index])
        
    # start time array at 0
    loom_start = time_array[0]
    for index in range(len(time_array)):
        time_array[index] = time_array[index] - loom_start

    for index in range(len(xposition_array)):
        distance_from_shelter.append(0)
        distance_from_shelter[index] = abs(xposition_array[index] - 28)
        
    # calculate x velocity
    xvelocity_array.append(0)
    for index in range(len(xposition_array)-1):
        position1 = xposition_array[index]
        position2 = xposition_array[index+1]
        velocity = (position2 - position1) / fs
        xvelocity_array.append(0)
        xvelocity_array[index+1] = velocity
        
    # find x velocity peaks
    max_velocity_time = (np.where(xvelocity_array == np.max(xvelocity_array))[0][0]
                         *0.04)
    max_velocity = np.max(xvelocity_array)
    peak_indices, _ = find_peaks(xvelocity_array, height = 4)
    for index in range(len(peak_indices)):
        peak_times.append(peak_indices[index] * 0.04)
        
        return xvelocity_array, time_array
            
def get_velocity_array_cohort2(path):
    filename = ''
    loom_index = int(0)
    stop_index = int(0)
    total_time = float(0)
    loom_start = 0
    frames = int(0)
    fs = float(0) 
    time_array = []
    xposition_array = []
    distance_from_shelter = []
    xvelocity_array = []
    peak_indices = []
    peak_times = []
    animal_id = ''
    loom_type = ''
    polyfit_function = None
    max_velocity_time = float(0)
    max_velocity = float(0)
    
    filename = path
    
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        current_line = []
        header_count = 0
        current_line = next(csv_reader)
        header_count = int(current_line[1])
        
        # iterate through csv until the "Animal Number" line is found
        for line in csv_reader:
            if line[0] == "Animal Number":
                animal_id = line[1]
            if line[0] == "Loom":
                loom_type = line[1]
            
                break
        
        # burn empty line in csv file
        next(file)
            
        df = pd.read_csv(file)
        
    fs = float(df['Trial time'][2])
    
    loom_index += 1
    for value in df[f'{loom_type} Loom']:
        if math.isnan(value):
            pass
        elif value == 0:
            loom_index += 1
        else:
            break
    
    total_time = 10
    frames = int(total_time/fs)
    stop_index = loom_index + frames
    
    time_array = list(df['Trial time'][loom_index:stop_index])
    xposition_array = list(df['X center'][loom_index:stop_index])
    
    
    # convert stings to floats
    for index in range(len(time_array)):
        time_array[index] = float(time_array[index])
        xposition_array[index] = float(xposition_array[index])
        
    # start time array at 0
    loom_start = time_array[0]
    for index in range(len(time_array)):
        time_array[index] = time_array[index] - loom_start
    
    for index in range(len(xposition_array)):
        distance_from_shelter.append(0)
        distance_from_shelter[index] = abs(xposition_array[index] - 28)
        
    # calculate x velocity
    xvelocity_array.append(0)
    for index in range(len(xposition_array)-1):
        position1 = xposition_array[index]
        position2 = xposition_array[index+1]
        velocity = (position2 - position1) / fs
        xvelocity_array.append(0)
        xvelocity_array[index+1] = velocity
        
    # find x velocity peaks
    max_velocity_time = (np.where(xvelocity_array == np.max(xvelocity_array))[0][0]
                         *0.04)
    max_velocity = np.max(xvelocity_array)
    peak_indices, _ = find_peaks(xvelocity_array, height = 4)
    for index in range(len(peak_indices)):
        peak_times.append(peak_indices[index] * 0.04)
        
    return xvelocity_array, time_array      
    
def plot(x1, x2, y1, y2, x_label, y_label, y_label2, title):
    # Plot both unprocessed demodulated stream            
    fig1 = plt.figure(figsize=(10, 6))
    ax0 = fig1.add_subplot(111)
    # Plotting the traces
    p0, = ax0.plot(x1, y1, linewidth=2, color='blue')

    ax0.set_ylabel(y_label)
    ax0.set_xlabel(x_label)
    ax0.set_xlim([0, 10])
    ax0.set_title(f'{title}')
    ax0.yaxis.set_ticks(np.arange(-2, 8, 2))
    
    ax1 = ax0.twinx()
    ax1.set_ylabel(y_label2)
    ax1.yaxis.set_ticks(np.arange(-20, 80, 10))
    p1, = ax1.plot(x2, y2, linewidth=2, color='red')    
    
    fig1.tight_layout()
    
    return(fig1, ax0, ax1)

file_list = os.listdir(cohort1_folder_name)

for index in range(len(file_list)):
    
    path = f'{cohort1_folder_name}\\{file_list[index]}'
    vel_array, time_array = get_velocity_array_cohort1(path)
    plot_dict[cohort1_order[index]].append(vel_array)

file_list = os.listdir(cohort2_folder_name)

for index in range(len(file_list)):
    
    path = f'{cohort2_folder_name}\\{file_list[index]}'
    vel_array, time_array = get_velocity_array_cohort2(path)
    plot_dict[cohort2_order[index]].append(vel_array)
    

for mouse in plot_dict.keys():
    
    print(mouse)
    fig, ax0, ax1 = plot(ts1, time_array, plot_dict[mouse][0], plot_dict[mouse][1], 'time (s)', 'Z-Score', 'Horizontal Velocity (cm/s)', f'{mouse} dLight signal / velocity')
    ax0.yaxis.set_ticks(np.arange(-4, 9, 2))
    ax1.yaxis.set_ticks(np.arange(-50, 101, 25))
    fig.savefig(f'{output_path}\\{mouse}.pdf', format='pdf')  