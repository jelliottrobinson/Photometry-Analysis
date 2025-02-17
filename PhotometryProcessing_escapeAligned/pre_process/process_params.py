# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 16:21:21 2021

This file contains parameters for processing data that are defined before
runtime. All parameter for general use of this program will be defined here or 
prompted during runtime.

General Workflow:
    1. Define parameters here. Default parameters are provided at the bottom of 
       this file if needed.
    2. Run main_pre_process and provide parameters when prompted.
    3. Run main - use the variable expolorer to access the epoch_stats variable
       to copy any data needed for further analysis.

@author: FISXV1
"""

#%% Pre-processing Parameters

'''
PP_INPUT: String 
Full path to a TDT data folder to pre-process a single run, or a folder 
containing multiple TDT data folders to pre-process multiple runs. TDT data 
folders processed together will be processed with the same settings and use the
same inputs collected at runtime.

PP_OUTPUT: String 
Full path to a folder where the pre-processed file will be 
saved.

TRANGE: List
Time range for epoch periods in format [start time (s), total time (s)]
The start time is relative to the ttl marking an epoch. Generally, a negative 
number is used to select a range that includes some period of time before the 
epoch onset to capture a baseline period. The total time is the time captured 
beginning from start time. e.g. if TRANGE [-10, 21] the selected period will 
begin 10 seconds before the ttl and end 11 seconds after the ttl. 

BASELINE_PER: List
Baseline period for collecting the mean and standard deviation used for 
z-scoring the data in format [start time (s), end time(s). The start and end 
times are relative to the ttl marking the epoch. The period must fall within 
the TRANGE. e.g. if BASELINE = [-10, -1] the raw mV data from 10 seconds before
the ttl to 1 second before the ttl is selected for calculating the
z-scoring metrics.  

DOWNSAMPLE_RATE:  Integer
The binning size used when downsampling the raw data. 

SIGNAL: String
Channel where the raw signal data is stored in the TDT object 
    
ISOS: String
Channel where the raw isosbestic data is stored in the TDT object
'''

PP_INPUT = r'Z:\Austen\striatumHeterogeneityProject\Photometry\accumbensMedialShell\Loom\raw_escape'
PP_OUTPUT = r'Z:\Austen\striatumHeterogeneityProject\Photometry\accumbensMedialShell\Loom\pre_processed_escapeAligned'

TRANGE = [-10, 21] 
BASELINE_PER = [-10, -1]
DOWNSAMPLE_RATE = 10

SIGNAL = '_465A'
ISOS = '_405A'
EPOC = 'PC0_'

#%% Plotting Parameters

'''
MAIN_INPUT: String
Full path to a folder containing one or more pre-processed data files.

MAIN_OUTPUT: String
Full path to a folder where a pdf of the output plot will be saved.

FIG_SAVE: Boolean. 
If True, a copy of the output pdf will be saved to the MAIN_OUTPUT folder.

EXPERIMENT_NAME: String
Name of experiment will be included in the plot titles and output pdf.

EPOCH_AVG_STREAM: Boolean
If True, produces an averaged, z-score epoch plot. This is the primary output 
of main.

X_LIM: List
Bounds of the epoch plot x-axis
    
Y_LIM: List
Bound of the epoch plot y-axis

EPOCH_ONSET: Boolean
Produces a vertical line at the time of the ttl on the epoch plot.

EPOCH_AVG_HM(2): Boolean
Adds a heat map to the epoch average plot. EPOCH_AVG_HM2 produces a second heat
map with a second set of parameters.

HM_COLOR_LIM(2): List
Bounds of the heat map color scale (represents z-score).

HM_TIME_LIM(2): List
Bounds of the heat map time axis.

RAW_MV_STEAM: Boolean
Plots the raw data stream for checking data quality
    
RAW_MV_START: Integer or Float
Start time (s) relative to the beginning of recording. This is to cut off the 
artifact effect from turning on the LEDs.
'''

MAIN_INPUT = r'Z:\Austen\striatumHeterogeneityProject\Photometry\lateralAccumbens\House Light (5uWatt)\pre_processed'
MAIN_OUTPUT = r'Z:\Austen\striatumHeterogeneityProject\Photometry\GFP_LoomExperiments\Standard_Looms\pdfs\escapeAligned\-0.5 to 5 seconds' 
FIG_SAVE = False

EXPERIMENT_NAME = 'House Light' 

EPOCH_AVG_STREAM = False

X_LIM = [-1, 11]
Y_LIM = [-2, 14] 

EPOCH_ONSET = False

EPOCH_AVG_HM = False
HM_COLOR_LIM = [-1, 4]
HM_TIME_LIM = [-1, 3]

EPOCH_AVG_HM2 = False 
HM_COLOR_LIM2 = [-1, 5] 
HM_TIME_LIM2 = [1.25, 5.5] 

# Only set this to true if EPOCH_AVG_HM is set to false
EPOCH_MOUSE_HM = False
MOUSE_HM_COLOR_LIM = [0, 2] 
MOUSE_HM_TIME_LIM = [-0.5, 5] 

RAW_MV_STREAM = True
RAW_MV_START = 1 


#%% Advanced Plotting Parameters
'''
PEAK_START_TIME: Integer or Float
Start bound for peak search

PEAK_STOP_TIME: Integer or Float
Stop bound for peak search

AUC_THRESHOLD: Integer or Float
Parameter for calculating the area under the curve. The algorithm traverses the
curve from the detected peak in both directions. The end of the curve is found
when the curve transitions from a downward to an upward slope and the current
value is above the AUC_THRESHOLD. 

EPOCH_STATS: Boolean
If True, main produces a dictionary of data frames called epoch_stats that 
contains stats of the determined peak including the peak value, delay of peak 
relative to ttl onset, area under the curve and full width half max.
'''

PEAK_START_TIME = -1
PEAK_STOP_TIME = 0

AUC_THRESH_FOR = 1.5
AUC_THRESH_BACK = 1.5

EPOCH_STATS = True

#%% Default parameters
'''
PP_INPUT = r''
PP_OUTPUT = r''

TRANGE = [-10, 21] 
BASELINE = [-10, -1]
DOWNSAMPLE_RATE = 10

SIGNAL = '_465A'
ISOS = '_405A'

MAIN_INPUT = r''
MAIN_OUTPUT = r'' 
FIG_SAVE = False

EXPERIMENT_NAME = '' 

EPOCH_AVG_STREAM = True

X_LIM = [-1, 11] 
Y_LIM = [-1, 12] 

EPOCH_ONSET = False 
                    
EPOCH_AVG_HM = True 
HM_COLOR_LIM = [-1, 12] 
HM_TIME_LIM = [-1, 11] 

EPOCH_AVG_HM2 = False 
HM_COLOR_LIM2 = [-1, 1] 
HM_TIME_LIM2 = [-1, 12] 

RAW_MV_STREAM = False 
RAW_MV_START = 10 

PEAK_START_TIME = 0
PEAK_STOP_TIME = 0.5

AUC_THRESH_FOR = 1.5
AUC_THRESH_BACK = 1.5

EPOCH_STATS = True # Produces epoch stats and supporting plot
'''