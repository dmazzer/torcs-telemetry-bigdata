#!/usr/bin/env python3
"""
get_telemetry.py: TORCS telemetry file reader and Apache Spark Streaming injector

"""

__author__ = "Daniel Mazzer"
__copyright__ = "Copyright 2017"
__credits__ = ""
__license__ = "MIT"
__maintainer__ = "Daniel Mazzer"
__email__ = "dmazzer@gmail.com"


telemetry_file = '/usr/local/share/games/torcs/telemetry/Inferno.dat'
debug_file = 'file.dat'
# telemetry_data = open(telemetry_file, 'r')
# 
# print (telemetry_data.)



import time
def follow(thefile):
    thefile.seek(0,0)
    while True:
        line = thefile.readline()
#        debug_obj.writelines(line)
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    debug_obj = open(debug_file, 'w')
    while True:
        try:
            logfile = open(telemetry_file,'r')
            break
        except IOError:
            print('Wating for the simulation start')
            time.sleep(1)
            
    loglines = follow(logfile)
    for line in loglines:
        debug_obj.writelines(line)
#         print line,