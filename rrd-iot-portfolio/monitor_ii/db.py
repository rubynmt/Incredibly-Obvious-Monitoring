from datetime import datetime
import sqlite3
from sqlalchemy     import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative     import declarative_base

Base = declarative_base()

class EnvironmentTPH:
    __tablename__ = 'tph_storage'
    id = Column(Integer, primary_key=True)
    device_name = Column(String)
    device_mac = Column(String)
    device_serial = Column(String)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    created_at = Column(DateTime)

    def __init__(self):
        self.device_name = "UNKNOWN"
        self.device_mac = "ZZ:ZZ:ZZ:ZZ:ZZ:ZZ"
        self.device_serial = "UNKNOWN"
        self.temperature = 0
        self.pressure = 0
        self.humidity = 0
        self.created_at = datetime.now()


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


class Db:
    def __init__(self, filename):
        self.__filename = filename
        self.__table_name = 'cpu_loads'

    def __execute(self, query):
        """Helper function that opens database connection, performs query, then closes.
        """
        connection = sqlite3.connect(self.__filename)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

    def create(self):
        """Create a new database using the filename stored in this class.

        If the database already exists, it will print the error and continue.
        """
        self.__execute('CREATE TABLE IF NOT EXISTS ' + self.__table_name +
                       '([id] INTEGER PRIMARY KEY,'
                       '[load] DECIMAL, '
                       '[created_at] DATETIME)')

    def store_cpu_load(self, cpu_load):
        """Store a single CPU load value in the database.

        :param cpu_load: The cpu load value to store in the database.
        """
        self.__execute('INSERT INTO ' + self.__table_name +
                       '(id, load, created_at) '
                       f'VALUES (null, {cpu_load}, datetime())')

