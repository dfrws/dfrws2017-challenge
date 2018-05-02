#!/usr/bin/python

# quick script to dump field 2 from onhub diagnostic report

# typical imports
import os, sys
import string
import shutil

# safe file name
SAFE_FILE = string.ascii_uppercase + string.ascii_lowercase + string.digits + ' -'
SAVE_DIR  = 'ohdump'

# attempt to load parser from fake schema
try:
	import onhub_diagnostic_pb2
except:
	print "ERROR: need onhub_diagnostic_pb2 parser to dump files"
	sys.exit(1)

if len(sys.argv) < 2:
	print "ERROR: need to specify protobuf file\n    {} <myprotobuf>".format(sys.argv[0])
	sys.exit(1)

if os.path.isdir(SAVE_DIR):
	print "WARNING: SAVE_DIR {} exists".format(SAVE_DIR)
	yn = -1
	while yn not in ['Y', 'N']:
		yn = raw_input('Overwrite? (Y/N): ')
	if yn == 'N':
		print "ERROR: nowhere to save files"
		sys.exit(1)
	shutil.rmtree(SAVE_DIR)
os.mkdir(SAVE_DIR)
os.mkdir(os.path.join(SAVE_DIR, 'files'))
os.mkdir(os.path.join(SAVE_DIR, 'commands'))

pb = onhub_diagnostic_pb2.report()

with open(sys.argv[1], 'rb') as f:
	pb.ParseFromString(f.read())

for f in pb.files:
	fn = ''.join(x if x in SAFE_FILE else '_' for x in f.path)
	with open(os.path.join(SAVE_DIR, 'files', fn), 'wb') as ofp:
		ofp.write(f.contents)

for c in pb.commands:
	fn = ''.join(x if x in SAFE_FILE else '_' for x in c.command)
	with open(os.path.join(SAVE_DIR, 'commands', fn + str(c.retval)), 'wb') as ofp:
		ofp.write(c.stdout)

