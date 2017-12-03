#!/usr/bin/env python3
import psutil, time, sys, signal, os, json, pathlib, matplotlib.pyplot as plt

filename = "/home/julian/battery.log"

def presentResults():
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
    plt.show()
    fig.savefig("/home/julian/battery.log.png", dpi=300)

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

def saveData():
    global log
    db_file = open(filename, "w")
    db_file.write(json.dumps(log))
    db_file.close()

def signal_handler(signal, frame):
        if(signal == 2):
            presentResults()
        if (len(log) > 0 and log[len(log)-1] != [None,None,None]):
            # eine Lücke zum Graphen hinzufügen um zu verdeutlichen, dass hier die Aufzeichnung unterbrochen wurde
            log.append([None,None,None])
        saveData()
        sys.exit(0)

def getPercentage():
    return round(psutil.sensors_battery().percent,2)

def getPower():
    return psutil.sensors_battery().power_plugged

def getLoad():
    return os.getloadavg()[0]

def main():
    global log
    signal.signal(signal.SIGINT, signal_handler)
    restoreData()
    #log = [[True,99,0.2], [True,89,0.6], [True,60,0.1],[True,50,0.7],[True,40,0.7],[True,35,0.7],[True,30,0.7], [True,10,0.8], [True,59,0.8], [True,22,1.0]]
    while(True):
        # damit sichergestellt ist, dass zwischen zwei Programmaufrufen min. 60 Sekunden vergangen sind
        time.sleep(60)
        log.append([getPower(),getPercentage(),getLoad()])
        print(getPower(),"/",getPercentage(),"/",getLoad())

main()