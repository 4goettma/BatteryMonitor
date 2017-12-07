#!/usr/bin/env python3
import time, sys, signal, os, json, pathlib, matplotlib.pyplot as plt
if (os.name == 'posix'):
    import psutil
elif (os.name == 'nt'):
    print("Not implemented for this operation system.")
    exit(0)
    
    from ctypes import *
else:
    print("Not implemented for this operation system.")
    exit(0)

filename = "./battery.log"

def presentResults(showWindow):
    global log
    fig, ax = plt.subplots()
    # Twin the x-axis twice to make independent y-axes.
    axes = [ax, ax.twinx()]
    axes[0].set_xlabel("time in minutes")
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
    axes[1].set_ylabel("Wattage", color="Orange")
    axes[1].tick_params(axis="y", colors="Orange")
    if(showWindow): plt.show()
    fig.savefig(filename+".png", dpi=600)
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

# Performance-Problem: Bei unrealistisch großen Logs wird bei jedem Speichern der komplette Datensatz neu geschrieben
def saveData():
    global log
    db_file = open(filename, "w")
    db_file.write(json.dumps(log))
    db_file.close()

def signal_handler_SIGINT(signal, frame):
        if(signal == 2):
            if (len(log) > 0):
                presentResults(True)
        if (len(log) > 0 and log[len(log)-1] != [None,None,None,None]):
            # eine Lücke zum Graphen hinzufügen um zu verdeutlichen, dass hier die Aufzeichnung unterbrochen wurde
            log.append([None,None,None,None])
        saveData()
        sys.exit(0)

#Zwischendurch bereits Daten rendern
def signal_handler_SIGUSR1(signal, frame):
    presentResults(False)

#Zwischendurch bereits Daten sichern
def signal_handler_SIGUSR2(signal, frame):
    saveData()

def getPercentage():
    if (os.name == 'posix'):
        return round(psutil.sensors_battery().percent,2)
    elif (os.name == 'nt'):
        class PowerClass(Structure):
            _fields_ = [('ACLineStatus', c_byte),
                        ('BatteryFlag', c_byte),
                        ('BatteryLifePercent', c_byte),
                        ('Reserved1',c_byte),
                        ('BatteryLifeTime',c_ulong),
                        ('BatteryFullLifeTime',c_ulong)]
        powerclass = PowerClass()
        result = windll.kernel32.GetSystemPowerStatus(byref(powerclass))
        return powerclass.BatteryLifePercent

def getPower():
    if (os.name == 'posix'):
        return psutil.sensors_battery().power_plugged
    elif (os.name == 'nt'):
        class PowerClass(Structure):
            _fields_ = [('ACLineStatus', c_byte),
                        ('BatteryFlag', c_byte),
                        ('BatteryLifePercent', c_byte),
                        ('Reserved1',c_byte),
                        ('BatteryLifeTime',c_ulong),
                        ('BatteryFullLifeTime',c_ulong)]
        powerclass = PowerClass()
        result = windll.kernel32.GetSystemPowerStatus(byref(powerclass))
        return (powerclass.ACLineStatus == 1)

def getLoad():
    if (os.name == 'posix'):
        return os.getloadavg()[0]
    elif (os.name == 'nt'):
        return 0

def getWattage():
    # es wird einfach angenommen, dass ein angeschlossener Akku nicht entladen wird 
    w = int(open("/sys/class/power_supply/BAT0/power_now", "r").read()) / 1000000
    if (getPower()):
        return w
    else:
        return -1*w

def getTime():
    t = time.localtime()
    return str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)+"_"+str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec)

def main():
    global log
    signal.signal(signal.SIGINT, signal_handler_SIGINT)
    signal.signal(signal.SIGUSR1, signal_handler_SIGUSR1)
    signal.signal(signal.SIGUSR2, signal_handler_SIGUSR2)
    restoreData()
    print("Monitoring started.")
    while(True):
        # damit sichergestellt ist, dass zwischen zwei Programmaufrufen min. 60 Sekunden vergangen sind
        time.sleep(60)
        log.append([getTime(),getPower(),getPercentage(),getWattage()])
        print(getTime(),"/",getPower(),"/",getPercentage(),"/",getWattage())

main()
