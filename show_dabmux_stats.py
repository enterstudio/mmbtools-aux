#!/usr/bin/env python2
#
# present statistics from dabmux Stats Server
# to munin

import sys
import json
import socket
import os

SOCK_RECV_SIZE=10240

def connect():
    """Create a connection to the dabmux stats server

    returns: the socket"""

    sock = socket.socket()
    sock.connect(("localhost", 12720))

    version = json.loads(sock.recv(SOCK_RECV_SIZE))

    if not version['service'].startswith("ODR-DabMux"):
        sys.stderr.write("Wrong version\n")
        sys.exit(1)

    return sock

if len(sys.argv) == 1:
    sock = connect()
    sock.send("values\n")
    values = json.loads(sock.recv(SOCK_RECV_SIZE))['values']

    tmpl = "{ident:20}{maxfill:>8}{minfill:>8}{under:>8}{over:>8}"
    print(tmpl.format(
	ident="id",
	maxfill="max",
	minfill="min",
	under="under",
	over="over"))

    for ident in values:
        v = values[ident]['inputstat']
        print(tmpl.format(
	    ident=ident,
            maxfill=v['max_fill'],
            minfill=v['min_fill'],
            under=v['num_underruns'],
            over=v['num_overruns']))


elif len(sys.argv) == 2 and sys.argv[1] == "config":
    sock = connect()

    sock.send("config\n")

    config = json.loads(sock.recv(SOCK_RECV_SIZE))

    print(config['config'])
