#!/usr/bin/env python3
import psutil, time, sys, signal, os, json, pathlib, matplotlib.pyplot as plt

# 1 = every 1 seconds
sampleRate = 1

filename = "./battery_Time_Power_Percentage_BatteryWattage.log"

def renderResults():
    global log, res
    fig, ax = plt.subplots()
    # Twin the x-axis twice to make independent y-axes.
    axes = [ax, ax.twinx()]
    if (sampleRate == 1):
        axes[0].set_xlabel("time in seconds")
    else:
        axes[0].set_xlabel("time in 1/{0} minutes ({0} units = 1 minute)".format(int(60/sampleRate)))
    data = []
    for i in range(len(log)):
        data.append(log[i][2])
    axes[0].plot(data, marker="", linestyle="default", linewidth="0.33", color="Black")
    axes[0].set_ylabel("Battery Percentage", color="Black")
    axes[0].tick_params(axis="y", colors="Black")
    axes[0].grid(linestyle="dotted")

    data = []
    for i in range(len(log)):
        data.append(log[i][3])
    axes[1].plot(data, marker="", linestyle="default", linewidth="0.33", color="Orange")
    axes[1].set_ylabel("Battery Wattage", color="Orange")
    axes[1].tick_params(axis="y", colors="Orange")
    if (res != 0):
        fig.savefig(filename+".png", dpi=res)
    else:
        fig.savefig(filename+"_0300dpi.png", dpi=300)
        fig.savefig(filename+"_0600dpi.png", dpi=600)
        fig.savefig(filename+"_3000dpi.png", dpi=3000)
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
    res = 0
    if (len(sys.argv)>1):
        res = int(sys.argv[1])
    restoreData()
    renderResults()

main()