# -*- coding: utf-8 -*-

#%% Imports statements
# imports built-ins and external packages
#import numpy as np
import tdt
import os
import pickle
import numpy as np
# internal imports
from my_tdt_obj import MyTDT
from auto_populate import one_time_inputs
from process_params import PP_INPUT, PP_OUTPUT

#%% Define some variables for processing
# provide path to TDT raw data files
raw_data_path = PP_INPUT
# output of pre-processed data files
process_output_path = PP_OUTPUT
folder = os.listdir(raw_data_path)

# pre-process data
# path to data can be provided in three ways:
# 1. path to a single TDT file
# 2. path to a folder containing a single TDT file
# 3. path to a folder containing multiple TDT files


values = [1]
# populate onset with time delay between stimulus onset and escape time
# each delay value should be placed in a list within the list and they must 
# be ordered in the same order they are read in to python
onset = [[]]


# conditional statements checking which type of input was submitted
def get_input_mode(raw_data_path, process_output_path, folder):

    if 'StoresListing.txt' in folder: #checks if the path is a raw data folder
        tdt_data = tdt.read_block(raw_data_path)
        data = MyTDT(tdt_data)
        file_name = raw_data_path.split('\\')[-1]
        with open(f'{process_output_path}\\{file_name}.bin','wb') as f:
             pickle.dump(data, f)
    elif len(folder) == 1: #checks if the path is a folder containing one raw data folder
        tdt_data = tdt.read_block(f'{raw_data_path}\\{folder[0]}')
        data = MyTDT(tdt_data)
        file_name = folder[0]
        with open(f'{process_output_path}\\{file_name}.bin','wb') as f:
             pickle.dump(data, f)
    elif len(folder) > 1: #check if the path is a folder containing more than ore raw data folder
        key, exp_in = one_time_inputs()
        data = []
        for ind in range(len(folder)):
            tdt_data = tdt.read_block(f'{raw_data_path}\\{folder[ind]}')
            if folder[ind] == '1125-1R-240605-standardLoom-ttlsAtEnd':
                tdt_data.epocs.PC0_.onset = np.array([tdt_data.epocs.PC0_.onset[0]])
                tdt_data.epocs.PC0_.offset = np.array([tdt_data.epocs.PC0_.offset[0]])
                tdt_data.epocs.PC0_.data = np.array([tdt_data.epocs.PC0_.data[0]])
            tdt_data.epocs.PC0_['onset'] = (tdt_data.epocs.PC0_['onset'] + 
                                            onset[ind][0])
            tdt_data.epocs.PC0_['offset'] = (tdt_data.epocs.PC0_['offset'] + 
                                             onset[ind][0])
            temp_data = MyTDT(tdt_data, ttl_key_type = key, exp_input = exp_in)
            file_name = folder[ind]
            with open(f'{process_output_path}\\{file_name}.bin','wb') as f:
                 pickle.dump(temp_data, f)
            data.append(temp_data)
    else:
        print('The provided data is not in a recognized format')
        
    return(data, file_name)

if __name__ == '__main__':
    
    data, file_name = get_input_mode(raw_data_path, 
                                     process_output_path, folder)

