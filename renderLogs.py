#!/usr/bin/env python3
import psutil, time, sys, signal, os, json, pathlib, matplotlib.pyplot as plt

# 3 = every 3 seconds
sampleRate = 3

filename = "./battery_Time_Power_Percentage_BatteryWattage.log"

def renderResults():
    global log, res
    fig, ax = plt.subplots()
    # Twin the x-axis twice to make independent y-axes.
    axes = [ax, ax.twinx()]
    axes[0].set_xlabel("time in 1/"+str(int(60/sampleRate))+" minutes ("+str(int(60/sampleRate))+" units = 1 minute)")
    data = []
    for i in range(len(log)):
        data.append(log[i][2])
    axes[0].plot(data, marker="", linestyle="default", color="Black")
    axes[0].set_ylabel("Battery Percentage", color="Black")
    axes[0].tick_params(axis="y", colors="Black")
    axes[0].grid(linestyle="dotted")

    data = []
    for i in range(len(log)):
        data.append(log[i][3])
    axes[1].plot(data, marker="", linestyle="default", color="Orange")
    axes[1].set_ylabel("Battery Wattage", color="Orange")
    axes[1].tick_params(axis="y", colors="Orange")
    fig.savefig(filename+".png", dpi=res)
    fig.savefig(filename+".svg")

def restoreData():
    global log
    file = pathlib.Path(filename)
    if file.is_file():
        db_file = open(filename, "r")
        db = json.loads(db_file.read())
        db_file.close()
        log = db
    else:
        log = []

def main():
    global log, res
    res = 600
    if (len(sys.argv)>1):
        res = int(sys.argv[1])
    restoreData()
    renderResults()

main()