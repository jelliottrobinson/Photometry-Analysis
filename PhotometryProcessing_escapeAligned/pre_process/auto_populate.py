# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 15:49:41 2021

@author: FISXV1
"""

from exp_dict import ORDERED_EXP_DICT
#%% This function will be called in the case of batch processing
# This takes all user inputs at the beginning when called, and bypasses future
# user input prompts. This is called so that the user isn't asked for the same 
# information for every data file within the process folder. This is important 
# so that the user doesn't provide different information 

def one_time_inputs():
    ttl_key_type = None
    exp_input = None
    while ttl_key_type == None:       
        user_input = input('Choose the stimulus identifying method: \n'
                           '1: single stimulus\n'
                           '2: ttl pulsewidth\n'
                           '3: presentation order\n\n')
        if user_input == '1':
            ttl_key_type = 'single stimulus'
        elif user_input == '2':
            ttl_key_type = 'ttl pulse width'
        elif user_input == '3':
            ttl_key_type = 'presentation order'
        else:
            print('Input not recognized.')
        
    if ttl_key_type == 'single stimulus':
        exp_input = input('What is the exeriment stimulus/condition?\n\n')       
    elif ttl_key_type == 'ttl pulsewidth':
        pass
    elif ttl_key_type == 'presentation order':
        while exp_input == None: 
            choice = 1
            choices = []
            print('Choose the type of experiment: \n')
            for exp in ORDERED_EXP_DICT.items():
                print(f'{choice}: {exp[0]}\n')
                print(f'{exp[1].keys()}\n')
                choices.append(choice)
                choice += 1
            exp_input = int(input())
            if exp_input in choices:
                pass
            else:
                print('Input not recognized')
                exp_input = None
    
    return(ttl_key_type, exp_input)
        
