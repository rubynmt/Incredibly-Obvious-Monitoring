from datetime import datetime
from time import sleep

#import the ORM items
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import the Model classes for environmentTPH and base
from db import EnvironmentTPH, Base

# import the methods that will be used from the mypi file
from mypi import \
    get_serial, get_mac, get_host_name, \
    get_cpu_temp, get_gpu_temp, get_maximum_cpu_load