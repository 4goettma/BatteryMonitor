#!/usr/bin/env python3
import psutil, time, sys, signal, os, json, pathlib, matplotlib.pyplot as plt

filename = "./battery.log"

def renderResults():
    global log
    fig, ax = plt.subplots()
    # Twin the x-axis twice to make independent y-axes.
    axes = [ax, ax.twinx()]
    axes[0].set_xlabel("time in minutes")
    data = []
    for i in range(len(log)):
        data.append(log[i][1])
    axes[0].plot(data, marker="", linestyle="default", color="Black")
    axes[0].set_ylabel("Battery Percentage", color="Black")
    axes[0].tick_params(axis="y", colors="Black")
    axes[0].grid(linestyle="dotted")

    data = []
    for i in range(len(log)):
        data.append(log[i][2])
    axes[1].plot(data, marker="", linestyle="default", color="Orange")
    axes[1].set_ylabel("System Load", color="Orange")
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