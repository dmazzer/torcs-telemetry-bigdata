#!/usr/bin/env python3
"""
get_telemetry.py: TORCS telemetry file reader and parser

"""

__author__ = "Daniel Mazzer"
__copyright__ = "Copyright 2017"
__credits__ = ""
__license__ = "MIT"
__maintainer__ = "Daniel Mazzer"
__email__ = "dmazzer@gmail.com"


import os
import json
import time
import socket

telemetry_file = '/usr/local/share/games/torcs/telemetry/Inferno.dat'
debug_file_raw = 'telemetry_raw.dat'
debug_file_parsed = 'telemetry_parsed.dat'
torcs_path = '/usr/local/bin/torcs'

class Telemetry_Parser:
    """
        Class to parse telemetry data generated by Torcs.
        
        Telemetry data file is read in realtime and it's parsed line by line.
        Each line from the telemetry data file represents one telemetry read from all cars.
        The parser map the space delimited file into a Python dictionary.
        Each car have it's own key/value dictionary.
        
        TOTCS Telemetry Header: 
        time Distance3 Ax3 Ay3 Vaz3 Steer3 Throttle3 Brake3 Gear3 Speed3 LapTime3 RPM3 Fuel3 
        Distance4 Ax4 Ay4 Vaz4 Steer4 Throttle4 Brake4 Gear4 Speed4 LapTime4 RPM4 Fuel4 
        Distance5 Ax5 Ay5 Vaz5 Steer5 Throttle5 Brake5 Gear5 Speed5 LapTime5 RPM5 Fuel5 
        Distance6 Ax6 Ay6 Vaz6 Steer6 Throttle6 Brake6 Gear6 Speed6 LapTime6 RPM6 Fuel6 
        Distance7 Ax7 Ay7 Vaz7 Steer7 Throttle7 Brake7 Gear7 Speed7 LapTime7 RPM7 Fuel7 
        Distance8 Ax8 Ay8 Vaz8 Steer8 Throttle8 Brake8 Gear8 Speed8 LapTime8 RPM8 Fuel8 
        Distance9 Ax9 Ay9 Vaz9 Steer9 Throttle9 Brake9 Gear9 Speed9 LapTime9 RPM9 Fuel9
    
    """
    
    def __init__(self):
        
        self.parsed_line = 0
        self.telemetry_parameters = 12 # hardcoded in torcs
        self.car_numbers = list()
        
        self.stream_buffer = ''
        
        self.ss = UDP_Socket_Server()
        
        
    def follow(self, thefile):
        """ Works like the linux command tail. """
        
        thefile.seek(0,0)
        while True:
            line = self.line_parser(thefile.readline())
    #        debug_r_obj.writelines(line)
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def line_parser(self, telemetry_stream):
        """ Receive telemetry stream and return a full line of telemetry data. """
        
        if telemetry_stream:
            if telemetry_stream[-1] == '\n':
                parsed_line = self.stream_buffer + telemetry_stream
                self.stream_buffer = ''
                return parsed_line
            else:
                self.stream_buffer = self.stream_buffer + telemetry_stream
                return None
        else:
            return None
                        
    def parser(self, telemetry_string):
        """ Receive a single telemetry line and parse measures for each car.
            
            This is the desired resultant JSON:
            {"Car": 9, "time": "52.196000", "telemetry": {"Distance": "4.605865", "LapTime": "0.128001", ..., "Speed": "34.137680"}}
            
        """
         
        debug_r_obj.writelines(telemetry_string)
        
        # the first line is the telemetry header
        if self.parsed_line == 0:
    #         print(telemetry_string)
            self.header = telemetry_string.split()
            self.players = int( (len(self.header)-1)/self.telemetry_parameters )
            self.total_params = len(self.header)
            for x in range(1,self.players*self.telemetry_parameters,self.telemetry_parameters):
                self.car_numbers.append(self.header[x][-1])
               
            print('Players: ' + str(self.players))
            print('Car numbers: ' + str(self.car_numbers))
            print('Total telemetry parameters: ' + str(self.total_params))
        
        # the following lines are the telemetru data
        else:
            tdata = telemetry_string.split(' ')
            if (len(tdata)-1) != len(self.header) :
                print('Problem parsing stream (size mismatch')
            
           
            telemetry_parsed = list()

            for x, car in zip(range(0,self.players), self.car_numbers): # (0, '3')(1, '4')(2, '5')(3, '6')(4, '7')(5, '8')(6, '9')
                telemetry_parsed.append({'Car': int(car), 'time': float(tdata[0]), 'telemetry': {}})
                for k in range(1, self.telemetry_parameters+1): # 1..12
                    telemetry_parsed[x]['telemetry'][self.header[k][:-1]] = float(tdata[(x*self.telemetry_parameters)+k])
#                  
            # send telemetry by UDP.
            self.send_telemetry(telemetry_parsed)
            
            # for debug
            newline = (str(telemetry_parsed) + '\n')
            debug_p_obj.writelines(newline)

        self.parsed_line += 1
                 
    def send_telemetry (self, telemetry_list):
        """ For each car a JSON is created and transmitted using the UDP socket. """
        
        for x in range(0,len(telemetry_list)):
            self.ss.send_udp(json.dumps(telemetry_list[x])  + '\n')
    
    
class UDP_Socket_Server:
    """ Connect to an UDP server and send UDP data. """
    
    def __init__(self):
        
        self.udp_ip = '127.0.0.1'
        self.udp_port = 7000
        
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def send_udp(self, message):
        self.conn.sendto(message.encode(), (self.udp_ip, self.udp_port))

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
            print('Waiting for the simulation start')
            time.sleep(1)
            
    loglines = tp.follow(logfile)
    for line in loglines:
        if line is not None:
            tp.parser(line)
