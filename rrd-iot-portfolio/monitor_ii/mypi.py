#!/usr/bin/python
# ----------------------------------------------------------------------------
#
#  File    : mypi.py
#  Purpose : Functions to display Pi properties
#
#  If called directly outputs :
#  - Pi Model
#  - Revision number
#  - Serial number
#  - Python version
#  - I2C,SPI and Bluetooth status
#  - Mac address
#  - IP address
#  - CPU temperature
#  - GPU temperature
#  - and other information through extensions by A Gould/S Huijsen
#
# Author   : Matt Hawkins
# Date     : 06/12/2017
# Location : https://www.raspberrypi-spy.co.uk/
#
# Extensions to this code created or collated, or redeveloped as needed
#
# Author   : Adrian Gould
# Author   : Sander Huijsen
# Date     : 2020/10/25
# ----------------------------------------------------------------------------
from datetime import datetime, timedelta
import platform
import subprocess
import os
from sys import maxunicode
from socket import gethostname, socket
import random

try:
    import psutil
except ImportError:
    psutil = None


# Define functions


def get_host_name():
    # return platform.node()
    # return platform.uname()[1]
    return gethostname()


def get_model():
    # Extract Pi Model string
    try:
        my_model = open('/proc/device-tree/model').readline()
    except:
        my_model = "Error"

    return my_model


def get_serial():
    # Extract serial from cpuinfo file
    my_cpu_serial = "Error"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                my_cpu_serial = line[10:26]
        f.close()
    except:
        my_cpu_serial = "Error"

    return my_cpu_serial


def get_revision():
    # Extract board revision from cpuinfo file
    my_revision = "Error"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:8] == 'Revision':
                my_revision = line[11:-1]
        f.close()
    except:
        my_revision = "Error"

    return my_revision


def get_eth_name(type=None):
    # Get name of Ethernet interface
    options = ['enx', 'eth']
    interface = None
    if type == 'w':
        options = ['wla']
    if type == 'l':
        options = ['lo']
    try:
        for root, dirs, files in os.walk('/sys/class/net'):
            for dir in dirs:
                for option in options:
                    if dir[:3] == option:
                        interface = dir
    except:
        interface = "None"
    return interface


def get_mac(interface='eth0'):
    # Return the MAC address of named Ethernet interface
    try:
        line = open('/sys/class/net/%s/address' % interface).read()
    except:
        line = "None"
    return line[0:17]


def get_ip(interface='eth0'):
    # Read ifconfig.txt and extract IP address
    try:
        filename = 'ifconfig_' + interface + '.txt'
        os.system('ifconfig ' + interface + ' > /home/pi/' + filename)
        f = open('/home/pi/' + filename, 'r')
        line = f.readline()  # skip 1st line
        line = f.readline()  # read 2nd line
        line = line.strip()
        f.close()

        if line.startswith('inet '):
            a, b, c = line.partition('inet ')
            a, b, c = c.partition(' ')
            a = a.replace('addr:', '')
        else:
            a = 'None'

        return a

    except:
        return 'Error'


def get_cpu_temp():
    # Extract CPU temp
    try:
        temp = subprocess.check_output(['vcgencmd', 'measure_temp'])
        temp = temp[5:-3]
    except:
        temp = '0.0'
    temp = f"{float(temp):.2f}"
    return str(temp)


def get_gpu_temp():
    # Extract GPU temp
    try:
        temp = subprocess.check_output(
            ['cat', '/sys/class/thermal/thermal_zone0/temp'])
        temp = float(temp) / 1000
    except:
        temp = 0.0
    temp = f"{float(temp):.2f}"
    return temp


def get_ram():
    # free -m
    output = subprocess.check_output(['free', '-m'])
    lines = output.splitlines()
    line = str(lines[1])
    ram = line.split()
    # total/free
    return (ram[1], ram[3])


def get_disk():
    # df -h
    output = subprocess.check_output(['df', '-h'])
    lines = output.splitlines()
    line = str(lines[1])
    disk = line.split()
    # total/free
    return (disk[1], disk[3])


def get_cpu_speed():
    # Get CPU frequency
    try:
        output = subprocess.check_output(['vcgencmd', 'get_config', 'arm_freq'])
        output = output.decode()
        lines = output.splitlines()
        line = lines[0]
        freq = line.split('=')
        freq = freq[1]
    except:
        freq = '0'
    return freq


def get_boot_time():
    """Determines the time the device was started
    :return: datetime
    """
    booted_at = datetime.fromtimestamp(psutil.boot_time())
    return booted_at


def get_uptime():
    """Determines the amount of time the device has been
    running for in seconds
    :return: seconds (float)
    """
    booted_at = get_boot_time()
    current_at = datetime.now()
    uptime_seconds = (current_at - booted_at).total_seconds()
    uptime = timedelta(seconds=uptime_seconds)
    return uptime


def get_python():
    """Get current Python version

    :return: string
    """
    pythonv = platform.python_version()
    return pythonv


def get_spi():
    # Check if SPI bus is enabled
    # by checking for spi_bcm2### modules
    # returns a string
    spi = "False"
    try:
        c = subprocess.Popen("lsmod", stdout=subprocess.PIPE)
        gr = subprocess.Popen(["grep", "spi_bcm2"], stdin=c.stdout,
                              stdout=subprocess.PIPE)
        output = gr.communicate()[0]
        if output[:8] == 'spi_bcm2':
            spi = "True"
    except:
        pass
    return spi


def get_i2c():
    # Check if I2C bus is enabled
    # by checking for i2c_bcm2### modules
    # returns a string
    i2c = "False"
    try:
        c = subprocess.Popen("lsmod", stdout=subprocess.PIPE)
        gr = subprocess.Popen(["grep", "i2c_bcm2"], stdin=c.stdout,
                              stdout=subprocess.PIPE)
        output = gr.communicate()[0]
        if output[:8] == 'i2c_bcm2':
            i2c = "True"
    except:
        pass
    return i2c


def get_bt():
    # Check if Bluetooth module is enabled
    # returns a string
    bt = "False"
    try:
        c = subprocess.Popen("lsmod", stdout=subprocess.PIPE)
        gr = subprocess.Popen(["grep", "bluetooth"], stdin=c.stdout,
                              stdout=subprocess.PIPE)
        output = gr.communicate()[0]
        if output[:9] == b'bluetooth':
            bt = "True"
    except:
        pass
    return bt


def get_random_cpu_load():
    """This function returns a random CPU load which can be used if no
    actual CPU load can be determined.

    :return: A random CPU load value between 0% and 100%
    """
    load = random.gauss(55, 10)
    if load < 0:
        return 0.0
    elif load > 100:
        return 100.0
    else:
        return round(load, 1)


def get_maximum_cpu_load():
    """This function returns the maximum CPU load across all CPU cores
    or a random value if the actual CPU load can't be determined.

    :return: Actual CPU load if available, else a random CPU load
    """
    if psutil is not None:
        return max(psutil.cpu_percent(percpu=True))
    else:
        return get_random_cpu_load()


# Original found in:
# https://stackoverflow.com/questions/12523586/python-format-size-application
# -converting-b-to-kb-mb-gb-tb/37423778
def format_bytes(size, style="short"):
    """Formats the given value into Bytes, Kilobytes, Megabytes, ...
    Using Byte shorthand by default - B, KB, MB, ...

    :param size:
    :param style:
    :return:
    """
    power = 2 ** 10  # 2**10 = 1024
    n = 0
    short_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T',
                    5: 'P', 6: 'E', 7: 'Y'}
    long_labels = {0: ' ', 1: ' Kilo', 2: ' Mega', 3: ' Giga',
                   4: ' Tera', 5: ' Peta', 6: ' Exa', 7: ' Yotta'}
    short_end = "B"
    long_end = "bytes"
    while size > power:
        size /= power
        n += 1
    if style == "short":
        power_labels = short_labels.copy()
        suffix = short_end
    else:
        power_labels = long_labels.copy()
        suffix = long_end

    return size, power_labels[n] + suffix


def make_printable(text=""):
    """Replace non-printable characters in a string."""
    # build a table mapping all non-printable characters to None
    # replace 255 with maxunicode to map unprintable unicode characters
    max_character = 255
    NOPRINT_TRANS_TABLE = {
        i: None for i in range(0, max_character + 1) if not chr(i).isprintable()
    }
    # the translate method on str removes characters
    # that map to None from the string
    return text.translate(NOPRINT_TRANS_TABLE)


def draw_line(character="-", length=40):
    print(character * length)


if __name__ == '__main__':
    # Script has been called directly
    s = socket()
    deg = u'\u00b0'
    my_ram = get_ram()
    my_disk = get_disk()
    eth_name = get_eth_name()
    wifi_name = get_eth_name('w')
    local_name = get_eth_name('l')
    host_name = get_host_name()

    draw_line("-", 70)
    print(f"{'Host Name':<21}: {get_host_name()}")
    draw_line("-", 70)
    print(f"{'Pi Model':<21}: {make_printable(get_model())}")
    draw_line("-", 70)
    print(f"{'System':<21}: {platform.platform()}")
    print(f"{'Revision Number':<21}: {get_revision()}")
    print(f"{'Serial Number':<21}: {get_serial()}")
    print(f"{'Python version ':<21}: {platform.python_version()}")
    draw_line("-", 70)
    print(f"{'Booted up':<21}: {get_boot_time().strftime('%B %d, %Y')}")
    print(f"{'At':<21}: {get_boot_time().strftime('%H:%M:%S')}")
    print(f"{'Uptime':<21}: {get_uptime()}")
    print(f"{'Current CPU Load':<21}: {get_maximum_cpu_load()}")
    draw_line("-", 70)
    print(f"{'I2C enabled':<21}: {get_i2c()}")
    print(f"{'SPI enabled':<21}: {get_spi()}")
    print(f"{'Bluetooth enabled ':<21}: {get_bt()}")
    draw_line("-", 70)
    print(f"{'Ethernet Name':<21}: {eth_name}")
    print(f"{'Ethernet MAC Address':<21}: {get_mac(eth_name)}")
    print(f"{'Ethernet IP Address':<21}: {get_ip(eth_name)}")
    print(f"{'Wireless Name':<21}: {wifi_name}")
    print(f"{'Wireless MAC Address':<21}: {get_mac(wifi_name)}")
    print(f"{'Wireless IP Address':<21}: {get_ip(wifi_name)}")
    print(f"{'Local Name':<21}: {local_name}")
    print(f"{'Local MAC Address':<21}: {get_mac(local_name)}")
    print(f"{'Local  IP Address':<21}: {get_ip(local_name)}")
    draw_line("-", 70)
    print(f"{'CPU Clock  ':<21}: {get_cpu_speed()}MHz")
    print(f"{'CPU Temperature':<21}: {get_cpu_temp()}{deg}C")
    print(f"{'GPU Temperature':<21}: {get_gpu_temp()}{deg}C")
    print(f"{'RAM (Available) ':<21}: {my_ram[0]}MB ({my_ram[1]}MB)")
    print(f"{'Disk (Available) ':<21}: {my_disk[0]} ({my_disk[1]})")
    draw_line("-", 70)
