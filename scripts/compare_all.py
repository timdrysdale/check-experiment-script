#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compare multiple processed websocket dumps for the spinner experiment
see https://github.com/dpreid/pidui

Relies on file naming convention of
<type><number>-<stream>-<timestamp>-processed.json

Usage

./compare_all.py --root ../log --out ../log/summary --step 6


timothy.d.drysdale@gmail.com
17 January 2022
"""
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
from step_peaks import read_json, clean, get_peaks, shift_start
   

parser = argparse.ArgumentParser(description='Compare processed spinner files')
parser.add_argument('--root', dest='root', type=str, 
                    help='the root dir for the file collection')
parser.add_argument('--out', dest='out', type=str, 
                    help='the dir for the output files')

parser.add_argument('--step', dest='step', type=float, 
                    help='the step size')

args = parser.parse_args()
# traverse root directory, and list directories as dirs and files as files

data = {}

for root, dirs, files in os.walk(args.root):

   for name in files:
       
       path = os.path.join(root, name) #we need this to open the file
      
       n = str(pathlib.Path(name).with_suffix(''))
       
       tokens = n.split("-")
       if len(tokens) > 3:
           if tokens[3]=="processed" and tokens[1]=="data":
               expt = tokens[0]
               timestamp = tokens[2]
               
               # make sure object we are adding key to, exists
               if expt not in data:
                   data[expt] = {}
                   
               data[expt][timestamp] = read_json(path)
 

for expt in data.keys():
    print("\n%s"%expt)
    times = sorted(data[expt].keys(),reverse=True) #put newest first

    plt.figure()
    
    ta,da = clean(data[expt][times[0]])
    ta0,tap,dap = get_peaks(ta,da)
    
    t0s = []
    tp1s = []
    tp2s = []
    dp1s = []
    dp2s = []

    plt.plot([np.min(ta),ta0],[0,0], '0.8', label='previous') #include this for the sake of the legend
    
    for time in times[1:]:
        t,d = clean(data[expt][time])
        if len(t) > 0: #flat lines are cleaned away to nothing, so skip them
            t = shift_start(t,d,ta0)
            plt.plot(t,d,'0.8')
            t0,tp,dp = get_peaks(t,d)
            t0s.append(t0)
            tp1s.append(tp[0])
            tp2s.append(tp[1])
            dp1s.append(dp[0])
            dp2s.append(dp[1])

    #calculate statistics
    tp1min = np.min(tp1s) - ta0
    tp1max = np.max(tp1s) - ta0
    tp1avg = int(np.round(np.mean(tp1s)-ta0,0))

    tp2min = np.min(tp2s) - ta0
    tp2max = np.max(tp2s) - ta0
    tp2avg = int(np.round(np.mean(tp2s)-ta0,0))
    
    dp1min = np.min(dp1s) 
    dp1max = np.max(dp1s) 
    dp1avg = np.round(np.mean(dp1s),2) 

    dp2min = np.min(dp2s) 
    dp2max = np.max(dp2s)
    dp2avg = np.round(np.mean(dp2s),2)
    

    col_labels=['t1-t0','d1-d0','t2-t0','d2-d0']
    row_labels=['units','min','avg','max','last']
    table_vals=[
            ['(ms)','(rad)','(ms)','(rad)'],
            [tp1min, dp1min, tp2min, dp2min],
            [tp1avg, dp1avg, tp2avg, dp2avg],
            [tp1max, dp1max, tp2max, dp2max],
            [tap[0]-ta0, dap[0], tap[1]-ta0, dap[1]]
            ]
    plt.table(
            cellText=table_vals,
            colWidths = [0.1]*4,
            rowLabels=row_labels,
            colLabels=col_labels,
            loc=4 #'center right'
            
            )
      
    plt.plot(ta,da,'b:',label='latest')    

    dt=30
    dd=0.1
    plt.plot(ta0,0,'r+')
    plt.text(ta0+dt,0+dd, '(t0,d0)')
                           
    plt.plot(tap[0],dap[0],'r+')
    plt.text(tap[0]+dt,dap[0]+dd, '(t1,d1)')
    
    plt.plot(tap[1],dap[1], 'r+')                   
    plt.text(tap[1]+dt,dap[1]+dd, '(t2,d2)')
    
    plt.plot([np.min(ta),ta0,ta0,np.max(ta)],[0,0,args.step,args.step],'g:', label='step')
    

               
    plt.xlabel("time/s")
    plt.ylabel("position/rad")
    plt.title("%s - latest vs %d previous runs"%(expt,len(times)))
    plt.legend()
    plotlatestname=os.path.join(args.out,"%s-latest.png"%expt)
    plt.savefig(plotlatestname,dpi=300)
    plt.close()
      
      
