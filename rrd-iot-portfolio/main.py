from datetime import datetime
from time import sleep
import sys
sys.path.append('/.../Incredibly-Obvious-Monitoring/rrd-iot-portfolio/monitor_i')
from monitor_i import monitor
from monitor_i import database



def main():
    db = database.Db('cpu_loads.db')
    db.create()
    while True:
        load = monitor.get_maximum_cpu_load()
        db.store_cpu_load(load)
        print(datetime.now(), ' CPU load =', load)
        sleep(3)


if __name__ == '__main__':
    main()