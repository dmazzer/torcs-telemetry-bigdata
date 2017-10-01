#!/usr/bin/env python3
"""
get_telemetry.py: TORCS telemetry file reader and Apache Spark Streaming injector

"""

#time    Distance3    Ax3    Ay3    Vaz3    Steer3    Throttle3    Brake3    Gear3    Speed3    LapTime3    RPM3    Fuel3    Distance4    Ax4    Ay4    Vaz4    Steer4    Throttle4    Brake4    Gear4    Speed4    LapTime4    RPM4    Fuel4    Distance5    Ax5    Ay5    Vaz5    Steer5    Throttle5    Brake5    Gear5    Speed5    LapTime5    RPM5    Fuel5    Distance6    Ax6    Ay6    Vaz6    Steer6    Throttle6    Brake6    Gear6    Speed6    LapTime6    RPM6    Fuel6    Distance7    Ax7    Ay7    Vaz7    Steer7    Throttle7    Brake7    Gear7    Speed7    LapTime7    RPM7    Fuel7    Distance8    Ax8    Ay8    Vaz8    Steer8    Throttle8    Brake8    Gear8    Speed8    LapTime8    RPM8    Fuel8    Distance9    Ax9    Ay9    Vaz9    Steer9    Throttle9    Brake9    Gear9    Speed9    LapTime9    RPM9    Fuel9

__author__ = "Daniel Mazzer"
__copyright__ = "Copyright 2017"
__credits__ = ""
__license__ = "MIT"
__maintainer__ = "Daniel Mazzer"
__email__ = "dmazzer@gmail.com"


import os
import time

telemetry_file = '/usr/local/share/games/torcs/telemetry/Inferno.dat'
debug_file_raw = 'telemetry_raw.dat'
debug_file_parsed = 'telemetry_parsed.dat'
torcs_path = '/usr/local/bin/torcs'

def follow(thefile):
    thefile.seek(0,0)
    while True:
        line = thefile.readline()
#        debug_r_obj.writelines(line)
        if not line:
            time.sleep(0.1)
            continue
        yield line

class Telemetry_Parser:
    def __init__(self, filename=None):
        
        self.parsed_line = 0
        self.telemetry_parsed = dict()
        self.telemetry_parameters = 12 # hardcoded in torcs
        self.car_numbers = list()
        
    def parser(self, telemetry_string):
        debug_r_obj.writelines(telemetry_string)
        
        if self.parsed_line == 0:
    #         print(telemetry_string)
            self.header = telemetry_string.split()
            self.racers = int( (len(self.header)-1)/self.telemetry_parameters )
            for x in range(1,self.racers*self.telemetry_parameters,self.telemetry_parameters):
                self.car_numbers.append(x)
               
            print('Racers: ' + str(self.racers))
            print('Cars numbers: ' + str(self.car_numbers))
        
        else:
            tdata = telemetry_string.split()
            
            self.telemetry_parsed[self.header[0]] = tdata[0] # time
            
            # preparing to receive data from each racer (one dict for racer)
            for x in range(1,self.racers*self.telemetry_parameters,self.telemetry_parameters):
                self.telemetry_parsed[self.header[x][-1]] = {}
                
            # receiving each telemetry data from each racer individually 
            for x in range(1,len(tdata)):
                self.telemetry_parsed[self.header[x][-1]][self.header[x][:-1]] = tdata[x]
                
            newline = (str(self.telemetry_parsed) + '\n')
            debug_p_obj.writelines(newline)

        self.parsed_line += 1
                 


if __name__ == '__main__':
    print('## TORCS telemetry data processor ##')
    print('')

    tp = Telemetry_Parser()
    
    print('Deleting old telemetry file... ', end=''),
    if os.path.isfile(telemetry_file):
        if os.access(telemetry_file, os.W_OK):
            os.remove(telemetry_file)
            print('done')
        else:
            print('Impossible to delete file')
    else:
        print('file already deleted')
            
#     os.spawnl(os.P_NOWAIT, torcs_path)
    print('Starting TORCS - The Open Race Car Simulator')
    os.system(torcs_path + ' &') 
    
    print('Processing realtime telemetry data')
    debug_r_obj = open(debug_file_raw, 'w')
    debug_p_obj = open(debug_file_parsed, 'w')
    while True:
        try:
            logfile = open(telemetry_file,'r')
            break
        except IOError:
            print('Wating for the simulation start')
            time.sleep(1)
            
    loglines = follow(logfile)
    for line in loglines:
        tp.parser(line)
