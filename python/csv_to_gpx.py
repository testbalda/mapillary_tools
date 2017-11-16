import json
import re
import os
import datetime
import csv
 
def get_args():
    import argparse
    p = argparse.ArgumentParser(description='Convert Mapillary ios json format to gpx.')
    p.add_argument('csv_in', help='Input csv file')
    p.add_argument('path_out', help='Path to folder of gpx files.')
    p.add_argument('out_file_prefix', help='File prefix for the gpx traces.', default='trace')
    p.add_argument('time_diff_cutoff', help='Cut off value for the difference in seconds between the gpx traces', default=float("inf"))
    p.add_argument('col_ids', help='Column ids for time,lat,lon in this order', default='012')
    return p.parse_args()

def write_file(gpx_trace, filename):
    with open(filename, "w") as fout:
        fout.write(gpx_trace)
    
if __name__ == '__main__':
    args = get_args()
    
    t_col_id = int(args.col_ids[0])
    lat_col_id = int(args.col_ids[1])
    lon_col_id = int(args.col_ids[2])

    gpx = "<gpx>"
    gpx += "<trk>"
    gpx += "<name>IOS JSON to GPX</name>"
    gpx += "<trkseg>"
    
    last_date = ""
    gpx_trace_count = 0

    with open(args.csv_in, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            t_datetime = datetime.datetime.utcfromtimestamp(int(row[t_col_id])/1000)
            t = t_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
            lat = row[lat_col_id]
            lon = row[lon_col_id]
            
            current_date = t_datetime
        
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
                
            gpx += "<trkpt lat=\"" + lat + "\" lon=\"" + lon + "\">"
            #gpx += "<ele>" + str(data['MAPAltitude']) + "</ele>"
            gpx += "<time>" + t + "</time>"
            gpx += "</trkpt>"

            last_date = current_date

        gpx += "</trkseg>"
        gpx += "</trk>"
        gpx += "</gpx>"

        filename_out = os.path.join(args.path_out, args.out_file_prefix + '_' + str(gpx_trace_count) + '.gpx')
        write_file(gpx, filename_out)
