#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timothy.d.drysdale@gmail.com
17 January 2022
"""
#import argparse
import json
import numpy as np
#import re
import matplotlib.pyplot as plt
#import os
#import pathlib
from scipy.signal import find_peaks

def clean(data):
    #discard any data before the position is zeroed
    # this is typically the steady state from the previous step
    #which occasionally shows up
    t = np.array(data["t"])
    d = np.array(data["d"])
    try:
        start = np.min(np.where(d==0.0))
    
        t = t[start:] - t[start]
        d = d[start:]
        
        #remove any NaN in t, d
        t1 = t[~np.isnan(t)]
        d1 = d[~np.isnan(t)]
        
        t2 = t1[~np.isnan(d1)]
        d2 = d1[~np.isnan(d1)]       
        
        
        return(t2,d2)
        
    except ValueError:
        # there is no value at zero, possibly missed the step.
        return([],[])

def get_t0_index(t,d):
    
    return np.min(np.where(d>0))-1

def get_peaks(t,d): #times in ms
    #discard any data before the position is zeroed
    # this is typically the steady state from the previous step
    #which occasionally shows up
    peaks,_ = find_peaks(d)
    
    #find t0
    t0i = get_t0_index(t,d)

    return t[t0i],t[peaks],d[peaks]

def shift_start(t,d,new_t0):
    # shift the start of the step to t0
    old_t0 = t[get_t0_index(t,d)]
    diff = new_t0 - old_t0
    t = t + diff
    return t
    

def read_json(filename):
  with open(filename) as f:
    lines = f.readlines()

    for line in lines:
        if len(line)>1:

                y = json.loads(line)

                data={
                        "t":y["t"],
                        "d":y["d"],
                        "v":y["v"]
                      } 
                return data

    
if __name__=="__main__":
    #run tests

    # test clean() with data with no step in it
    data = read_json("./test/no_step.json")
    t,d = clean(data)
    assert len(t) == 0.0 #zero length array returned if no step
    
    #test clean() with NaN in the data
    data = read_json("./test/nan.json")
    assert len(data["t"]) == 8
    assert data["d"][-1] == 1 
    t,d = clean(data)
    assert len(t) == 6
    assert d[-1] == 0 #the last value in the file is 1, but the t value is nan
     
    # test clean() with non-zero data at start from a previous step
    data = read_json("./test/initial_step.json")
    assert len(data["t"]) == 376
    t,d = clean(data)
    assert len(t) == 342 # 34 samples deleted (was 376)
    assert t[0] == 0.0 #first value is zero

    #test get_t0
    t0i = get_t0_index(t,d)
    assert t0i == 42
    assert t[t0i] == 229
    
    #test get_peaks 
    t0,tp, dp = get_peaks(t,d)
    assert t0 == 229
    assert tp[0] == 414
    assert tp[1] == 783
    assert dp[0] == 9.25
    assert dp[1] == 6.81
    plt.plot(t,d)
    plt.plot(t0,0,'r+')
    plt.plot(tp,dp,'r+')
    plt.xlabel('time/ms')
    plt.ylabel('position/rad')
    plt.savefig('./test/peaks.png')
    plt.close()
    
    data = read_json("./test/normal.json")
    tn,dn = clean(data)
    tn = shift_start(tn,dn,t0)
    tn0,tnp,dnp = get_peaks(tn,dn)

    assert tn0 == 229
    assert tnp[0] == 409
    assert tnp[1] == 784
    assert dnp[0] == 9.23
    assert dnp[1] == 6.8
    
    plt.figure()
    plt.plot(t,d,'r')
    plt.plot(t0,0,'r+')
    plt.plot(tp,dp,'r+')
    plt.plot(tn,dn,'b:')
    plt.plot(tn0,0,'b+')
    plt.plot(tnp,dnp,'b+')    
    plt.xlabel('time/ms')
    plt.ylabel('position/rad')
    plt.savefig('./test/shift.png')
    

    
    
    
    
    
    
    
  