#!/usr/bin/env python

import json
import re
import os
import datetime

def get_args():
    import argparse
    p = argparse.ArgumentParser(description='Convert Mapillary ios json format to gpx.')
    p.add_argument('path_in', help='Path to folder of json files.')
    p.add_argument('path_out', help='Path to folder of gpx files.')
    p.add_argument('out_file_prefix', help='File prefix for the gpx traces.', default='trace')
    p.add_argument('time_diff_cutoff', help='cut off value for the difference in seconds between the gpx traces', default=float("inf"))
    return p.parse_args()

def write_file(gpx_trace, filename):
    with open(filename, "w") as fout:
        fout.write(gpx_trace)
    
if __name__ == '__main__':
    args = get_args()

    gpx = "<gpx>"
    gpx += "<trk>"
    gpx += "<name>IOS JSON to GPX</name>"
    gpx += "<trkseg>"

    pattern = re.compile("^(\d*)_(\d*)_(\d*)_(\d*)_(\d*)_(\d*)_*")
    
    last_date = ""
    gpx_trace_count = 0
    
    all_meta = [x for x in os.listdir(args.path_in)]

    all_meta.sort()
    
    for fn in all_meta:
        filename_in = os.path.join(args.path_in, fn)
        t = fn[:-5]

        if t == "history":
            continue

        match = pattern.match(t)
    
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        hour = match.group(4)
        minute = match.group(5)
        second = match.group(6)
       
        current_date = datetime.datetime.strptime(match.group(0), '%Y_%m_%d_%H_%M_%S_')
        
        if last_date=="" : last_date = current_date
        
        if abs((last_date-current_date).total_seconds()) > float(args.time_diff_cutoff):        
            gpx += "</trkseg>"
            gpx += "</trk>"
            gpx += "</gpx>"
            filename_out = os.path.join(args.path_out, args.out_file_prefix + '_' + str(gpx_trace_count) + '.gpx')
            write_file(gpx, filename_out)
            gpx_trace_count+=1
            gpx = "<gpx>"
            gpx += "<trk>"
            gpx += "<name>IOS JSON to GPX</name>"
            gpx += "<trkseg>"

        t = "{}-{}-{}T{}:{}:{}Z".format(year, month, day, hour, minute, second)
        if os.path.isfile(filename_in):
            with open(filename_in, "r") as f:
                data = json.load(f)
                if 'MAPLatitude' in data and 'MAPLongitude' in data and 'MAPAltitude' in data:
                    gpx += "<trkpt lat=\"" + str(data['MAPLatitude']) + "\" lon=\"" + str(data['MAPLongitude']) + "\">"
                    gpx += "<ele>" + str(data['MAPAltitude']) + "</ele>"
                    gpx += "<time>" + t + "</time>"
                    gpx += "</trkpt>"
                else:
                    print(filename_in)
         
               
        last_date = current_date

    gpx += "</trkseg>"
    gpx += "</trk>"
    gpx += "</gpx>"

    filename_out = os.path.join(args.path_out, args.out_file_prefix + '_' + str(gpx_trace_count) + '.gpx')
    write_file(gpx, filename_out)
    gpx_trace_count+=1    
    
    