#!/usr/bin/env python

import os
import argparse
import random

def run(cmd):
    os.system(" ".join(cmd))

def get_args():
    p = argparse.ArgumentParser(description='Sample and geotag video with location and orientation from GPX file.')
    p.add_argument('video_file', help='File path to the data file that contains the metadata')
    p.add_argument('--image_path', help='Path to save sampled images.', default="video_samples")
    p.add_argument('--sample_interval', help='Time interval for sampled frames in seconds', default=1, type=float)
    p.add_argument('--gps_trace', help='GPS track file')
    p.add_argument('--time_offset', help='Time offset between video and gpx file in seconds', default=0, type=float)
    p.add_argument("--skip_sampling", help="Skip video sampling step", action="store_true")
    p.add_argument("--skip_upload", help="Skip upload images", action="store_true")
    p.add_argument("--user", help="User name")
    p.add_argument("--userkey", help="User key")
    p.add_argument("--email", help="User email")
    p.add_argument("--project", help="Specify project for the video", default=None)
    p.add_argument("--project_key", help="Specify project key for the video", default=None)
    p.add_argument("--video_start_time", help="Specify the video start time",default=None)
    p.add_argument('--offset_angle', default=0., type=float, help='offset camera angle (90 for right facing, 180 for rear facing, -90 for left facing)')
    p.add_argument("--image_prefix", help="Specify the prefix for the images, to avoid same names", default=str(int(random.random()*1000000)))

    return p.parse_args()

if __name__ == "__main__":

    args = get_args()

    if os.path.exists(os.path.join(args.image_path, "PROCESSING_LOG.json")) is False:
        cmd = ["python", "geotag_video.py",
               args.video_file,
               "--gps_trace", args.gps_trace,
               "--image_path", args.image_path,
               "--sample_interval", str(args.sample_interval)]
        if args.video_start_time:
            cmd.extend(["--video_start_time", str(args.video_start_time)])
        if args.offset_angle:
            cmd.extend(["--offset_angle", str(args.offset_angle)])
        if args.image_prefix:
            cmd.extend(["--image_prefix", str(args.image_prefix)])

        run(cmd)

    assert(args.user is not None and (args.email is not None or args.userkey is not None))

    
    upload_cmd = [
        "python", "upload_with_preprocessing.py",
        args.image_path,
        "--remove_duplicates",
        "--interpolate_directions",
        "--duplicate_distance", "0.5",
        "--duplicate_angle", "360",
        "--user", args.user,
    ]
    if args.email:
        upload_cmd.extend(["--email", args.email])
    if args.project:
        upload_cmd.extend(["--project", repr(args.project)])        
    if args.project_key:
        upload_cmd.extend(["--project_key", args.project_key])      
    if args.offset_angle:
        upload_cmd.extend(["--offset_angle", str(args.offset_angle)])
    if args.userkey:
        upload_cmd.extend(["--userkey", args.userkey])  
    if args.skip_upload:
        upload_cmd.append("--skip_upload")
    

    run(upload_cmd)
