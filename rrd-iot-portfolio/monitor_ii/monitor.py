import random
from datetime import datetime
from time import sleep

try:
    import psutil
except ImportError:
    psutil = None


def get_random_cpu_load():
    """Return a random CPU load. It has a Gaussian distribution
    with a mean of 55 and a standard deviation of 10.
    """
    cpuload = random.gauss(55, 10)
    if cpuload <= 0:
        return 0
    elif cpuload >= 100:
        return 100
    else:
        return cpuload


def get_maximum_cpu_load():
    """Get maximum cpu load from the system. Returns a random
    CPU load if the system can't provide it.
    """
    if psutil:
        return max(psutil.cpu_percent(percpu=True))
    else:
        return get_random_cpu_load()

while True:
    load = get_maximum_cpu_load()
    print(datetime.now(), ' CPU load =', load)
    sleep(3)