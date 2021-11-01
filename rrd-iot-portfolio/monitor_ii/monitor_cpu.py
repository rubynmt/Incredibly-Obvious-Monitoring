from datetime import datetime
from time import sleep

# import the ORM items
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import the Model classes for CPU and Storage
from db import CPU, Storage, Base

# import the methods that will be used from the mypi file
from mypi import \
    get_serial, get_mac, get_host_name, \
    get_cpu_temp, get_gpu_temp, get_maximum_cpu_load


db_filename = './data/monitor_data.db'


def headings():
    print()
    print(f'{"Name":<10}|{"Serial #":<18}|'
          f'{"MAC":<20}|{"Created at":<28}|'
          f'{"CPU Temp":>8}|{"GPU Temp":>8}|'
          f'{"CPU Load":>8}'
          f'')


def main(_delay):
    engine = create_engine(f'sqlite:///{db_filename}')
    session = sessionmaker(bind=engine)()
    Base.metadata.create_all(engine)
    counter = 0

    while True:
        # Create a CPU object and set the properties
        cpu = CPU()
        cpu.host_name = get_host_name()
        cpu.serial = get_serial()
        cpu.host_mac = get_mac()
        cpu.load = get_maximum_cpu_load()
        cpu.cpu_temp = get_cpu_temp()
        cpu.gpu_temp = get_gpu_temp()
        cpu.created_at = datetime.now()
        # save the object to the database using SQLAlchemy ORM and
        # commit the action
        session.add(cpu)
        session.commit()

        last_readings = session.query(CPU).order_by(CPU.id.desc()).first()

        if counter % 10 == 0:
            headings()
        counter += 1

        print(f'{last_readings.host_name:<10}|{last_readings.serial:<18}|'
              f'{last_readings.host_mac:^20}|{last_readings.created_at}  |'
              f'{last_readings.cpu_temp:>8.1f}|{last_readings.gpu_temp:>8.1f}|'
              f'{last_readings.load:>8.1f}'
              f'')

        sleep(_delay)


if __name__ == '__main__':
    delay = 5.0
    main(delay)
