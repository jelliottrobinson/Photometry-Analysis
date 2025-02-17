# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 16:20:56 2021

@author: FISXV1
"""


# Dictionary of experiments where the ttl pulse width codes for a certain 
# experimental stimulus
# The keys refer to the ttl pulsewidth (s), values are the stimulus

EXP_DICT = {
    
    'multicolor': {0.001: 'UV', 
                   0.005: 'Cyan', 
                   0.01:  'Green',
                   0.02:  'Red', 
                   0.03:  'House Light'},
    
    'mc_NIR':     {0.001: 'UV', 
                   0.005: 'Cyan', 
                   0.01:  'Green', 
                   0.02:  'Red',
                   0.05:  'NIR'},
    
    'mc_nohouse': {0.001: 'UV', 
                   0.005: 'Cyan', 
                   0.01:  'Green', 
                   0.02:  'Red'},
    
    '3 Tones': {0.01: '6kHz',
                0.05: '8kHz',
                0.1: '12kHz'},
    
    '5x1LightPulse_1000sIPI': {0.001: 'Pre-300x 0.5Hz Light Pulses',
                               0.004: 'Post-300x 0.5Hz Light Pulses'},
    
# =============================================================================
#     '4 Tones': {0.001: '1kHz', 
#                    0.005: '2kHz', 
#                    0.01:  '4kHz', 
#                    0.02:  '16kHz'},
# =============================================================================
    
    '1s1s5min1s_HouseLight': {0.01: '1s Following 1s',
                              0.02: '1s Following 5min',
                              0.03: 'Initial 1s',
                              0.04: 'Initial 5min'},
    
    'NIR':        {0.001: 'NIR', 
                   0.005: 'House Light'},
    
    'cyan_green_red' : {0.005: 'Cyan', 
                        0.01: 'Green', 
                        0.02: 'Red'},
    
    'HouseLight_Low_High' : {0.002: 'Low',
                             0.003: 'High'},
    
    'HouseLight_LowWithFilter_None' : {0.003: 'Low with Filter',
                                       0.004: 'No Stimulus'}
}

# Dictionary of experiments where multiple stimuli are presented in a known 
# order; the ttl pulse width is constant

ORDERED_EXP_DICT = {
    
    'long_fade_in':  {'Instantaneous': [1,6,9,15,22], 
                      '0.5 Seconds': [5,7,8,11,23], 
                      '1 Second': [10,12,13,17,19], 
                      '2 Seconds': [3,4,14,16,20], 
                      '10 Seconds': [0,2,18,21,24]},
    
    'short_fade_in': {'0.05 Seconds': [7,12,14,18,22],
                      '0.1 Seconds': [10,11,16,20,24],
                      '0.2 Seconds': [8,13,17,19,21],
                      '0.3 Seconds': [0,2,6,9,15],
                      '0.4 Seconds': [1,3,4,5,23]},   
    
    'combined_fade_in' : {'0.05 Seconds': [1,11,18,22,23],
                          '0.4 Seconds': [2,7,14,16,24],
                          '1 Second': [6,8,12,13,19],
                          '2 Seconds': [0,3,4,15,21],
                          '10 Seconds': [5,9,10,17,20]}
    
}


