# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 20:28
# @Author  : Adesun
# @Site    : https://github.com/Adesun
# @File    : log_parser.py

import argparse
import logging
import os
import platform
import re
import sys


import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def parse_args():
    parser = argparse.ArgumentParser(description="training map plotter by Hooman ")
    parser.add_argument('--checkpoints', dest='path2Checkpoints', type=str, help='path to model checkpoints')
    parser.add_argument('--darknet', dest='path2Darknet', type=str, help='path to darknet executable')
    parser.add_argument('--data', dest='dataFilePath', type=str, help='full path to data file')
    parser.add_argument('--config', dest='configFilePath', type=str, help='full path to config file')
    parser.add_argument('--save', dest='plotSavePath', type=str, help='path to save results')

    return parser.parse_args()


def hsParse2GetMap(res):
    calcMap = -0.0
    try:
        resSp = res.split("\n")
        look4 = "mean average precision ("
        for rl in resSp:
            if look4 in rl:
                mapSp = rl.split("=")
                calcMap = float(mapSp[-1].split(",")[0])
    except:
        print("Error: failed to parse string to find map")
            
    return calcMap

def calcMaps(args):
    cp_names = []
    cp_maps = []

    cpDic = {}
    for nm in os.listdir(args.path2Checkpoints):
        val = int(nm.split("_")[1].split(".")[0])
        cpDic[val] = str(nm)
    
    keysList = list(cpDic.keys())
    keysList.sort()
    for weightKey in keysList:
        cmd = args.path2Darknet + 'darknet detector map ' + args.dataFilePath + \
        ' ' + args.configFilePath +' '+ args.path2Checkpoints + cpDic[weightKey]
    

        res = os.popen(cmd).read()
        calcMap = hsParse2GetMap(res)

        #cp_names.append(cpDic[weightKey])
        cp_names.append(str(weightKey))
        cp_maps.append(calcMap)


    # for i in range(len(cp_maps)):
    #     print("\n\n\n****HS******\n")
    #     print("for:   " + cp_names[i] + "   found:  " + str(cp_maps[i]))

    return cp_names, cp_maps
   
def hsMapPlotter(args):
    cp_names, cp_maps = calcMaps(args)

    fig, ax = plt.subplots()
    # set area we focus on
    ax.set_ylim(0, 8)

    major_locator = MultipleLocator()
    minor_locator = MultipleLocator(0.5)
    ax.yaxis.set_major_locator(major_locator)
    ax.yaxis.set_minor_locator(minor_locator)
    ax.yaxis.grid(True, which='minor')

    ax.plot(cp_names, cp_maps)
    plt.xlabel('checkpoint')
    plt.ylabel('map')
    plt.tight_layout()

    plt.savefig(args.plotSavePath + 'validPlot.svg', dpi=300, format="svg")

    saveF = open(args.plotSavePath + 'validMaps.txt', 'w')
    for i in range(len(cp_maps)):
        saveF.write(str(cp_names[i]) + ',' + str(cp_maps[i]) + '\n')
    saveF.close()



if __name__ == "__main__":
    args = parse_args()
    hsMapPlotter(args)

'''
clear;python hs_map_plotter.py --darknet '/home/hooman/darknet_alex/' --data '/home/hooman/darknet_alex/mapTests/headData.data' --config '/home/hooman/darknet_alex/hsHeadDetector_darkPreTrained/config/detectHead.cfg' --checkpoints '/home/hooman/darknet_alex/mapTests/checkpointWeights/' --save '/home/hooman/darknet_alex/mapTests/'
'''