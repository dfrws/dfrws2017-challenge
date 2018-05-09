#!/usr/bin/python3

import os
import sys
import json
import requests
import argparse
import datetime

def do_files(onhub):
    if not args.directory:
        print("Specify the directory to drop the files")
        exit(1)

    for entry in onhub['files']:
        if "content" not in entry.keys():
            continue
        path = "%s/%s" % (args.directory, entry["path"])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(entry["content"])

        print("Created file %s" % (path))

def do_networkConfig(onhub):
    print(onhub["networkConfig"])

def do_wanInfo(onhub):
    print(onhub["wanInfo"])

def do_commandOutputs(onhub):
    for entry in onhub['commandOutputs']:
        if "output" not in entry.keys():
            continue
        print(entry["command"])
        print(entry["output"])

def do_stations(onhub):
    stations = onhub["infoJSON"]["_apState"]["_stations"]
    for entry in stations:
        print("'%s' (%s), last seen on %s" %
            (entry["_dhcpHostname"], ", ".join(entry["_ipAddresses"]),
             datetime.datetime.utcfromtimestamp(entry["_lastSeenSecondsSinceEpoch"]).isoformat()))
 
handlers = [do_files, do_networkConfig, do_wanInfo, do_commandOutputs, do_stations]
    

def main():
    parser = argparse.ArgumentParser(description='Parser for Google OnHub logs')
    parser.add_argument('-d' '--directory', dest="directory", help='directory to store extracted files')
    parser.add_argument('target', help='data to extract (%s)' % (", ".join([f.__name__[3:] for f in handlers])));

    global args
    args = parser.parse_args()
    onhub = json.load(sys.stdin)

    for h in handlers:
        if h.__name__ != "do_" + args.target:
            continue
        h(onhub)
        return(0)

    print("Unsupported target (%s)" % args.target)
    return(1)

main()
