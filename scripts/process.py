#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process websocket dumps for the spinner experiment
see https://github.com/dpreid/pidui

timothy.d.drysdale@gmail.com
17 January 2022
"""
import argparse
import json
import numpy as np

import matplotlib.pyplot as plt
#import termplotlib as tpl
from uniplot import plot

parser = argparse.ArgumentParser(description='Read JSON data file for spinner.')
parser.add_argument('--file', dest='filename', type=str, 
                    help='the name of the datafile')

args = parser.parse_args()
t = []
d = []
v = []

filename = args.filename

with open(filename) as f:
    lines = f.readlines()
    
    for line in lines:
        if len(line)>1:

            try:
                y = json.loads(line)
                t.extend(y["t"])
                d.extend(y["d"])
                v.extend(y["v"])
                
            except:
               pass
    # Dump data to file
    
    data = {
                "t":t,
                "d":d,
                "v":v
            }
    
    outfilename = filename.replace(".json", "-processed.json")
    
    with open(outfilename, 'w') as outfile:
        json.dump(data, outfile)
        
    #termplot
    #fig = tpl.figure()
    #fig.plot(t,d, width=79, height=30)
    #fig.show()
    
    #uniplot
    tp =np.array(t)/1000
    tp = tp - tp[0]
    dp = np.array(d)
    vp = np.array(v)
    #plot(xs=[tp,tp], ys=[dp,vp/20], lines=True, x_unit=" s", y_unit=" rad",title="%s"%(filename),legend_labels=['d','v/20'])
    plot(xs=tp, ys=dp, lines=True, x_unit=" s", y_unit=" rad",title="%s"%(filename),legend_labels='d')
    
    plt.plot(tp,dp)
    plt.xlabel("time/s")
    plt.ylabel("position/rad")
    plt.title(filename)
    plotfilename = filename.replace(".json", ".png")
    plt.savefig(plotfilename, dpi=300)
    
