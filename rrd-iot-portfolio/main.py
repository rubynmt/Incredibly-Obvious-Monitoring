from datetime import datetime
from time import sleep
import sys
sys.path.append('/.../Incredibly-Obvious-Monitoring/rrd-iot-portfolio/monitor_i')
from monitor_i import monitor
from monitor_i import database
from tabulate import  tabulate

def main():
    db = database.Db('cpu_loads.db')
    db.create()
    count = 0
    data = []

    while count <= 10:
        load = monitor.get_maximum_cpu_load()
        db.store_cpu_load(load)
        data.append([datetime.now().date(), datetime.now().time(), load])
        table = monitor.displayCPUTable(data)
        print(table +'\n')
        sleep(3)
        count += 1


if __name__ == '__main__':
    main()