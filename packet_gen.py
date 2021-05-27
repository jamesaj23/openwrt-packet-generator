import socket
import struct

import scapy.all as scapy

# Helper method to obtain IP of our router
def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
            

def generate_packets():
    """Handler function to create our desired packets."""
    # packets = []
    scapy.send(scapy.IP(dst=str(get_default_gateway_linux()))/scapy.ICMP())
    scapy.sendp("I'm travelling on python")


def generate_end_of_transmission():
    scapy.sendp("End Transmission")
