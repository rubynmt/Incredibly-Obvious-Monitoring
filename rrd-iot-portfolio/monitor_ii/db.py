from datetime import datetime

from sqlalchemy     import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative     import declarative_base

Base = declarative_base()


class CPU(Base):
    __tablename__ = 'device_general'
    id = Column(Integer, primary_key=True)
    host_name = Column(String)
    serial = Column(String)
    host_mac = Column(String)
    load = Column(Float)
    cpu_temp = Column(Float)
    gpu_temp = Column(Float)
    created_at = Column(DateTime)

    def __init__(self):
        self.host_name = "UNKNOWN"
        self.host_mac = "ZZ:ZZ:ZZ:ZZ:ZZ:ZZ"
        self.created_at = datetime.now()
        self.serial = "UNKNOWN"
        self.load = -999.99
        self.cpu_temp = -999.99
        self.gpu_temp = -999.99


class Storage(Base):
    __tablename__ = 'device_storage'
    id = Column(Integer, primary_key=True)
    host_name = Column(String)
    host_mac = Column(String)
    total_storage = Column(Integer)
    free_storage = Column(Integer)
    used_storage = Column(Integer)
    created_at = Column(DateTime)

    def __init__(self):
        self.host_name = "UNKNOWN"
        self.host_mac = "ZZ:ZZ:ZZ:ZZ:ZZ:ZZ"
        self.created_at = datetime.now()
        self.total_storage = None
        self.free_storage = None
        self.used_storage = None
