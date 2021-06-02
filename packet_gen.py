import socket
import struct
import logging
import sys

import tqdm
import scapy.all as scapy

LOGGER = logging.getLogger()

DATA_FILE_PATH = ""
BUFFER_SIZE = 1024
DESTINATION_HOST = "192.168.20.13"
DESTINATION_PORT = 5001


# Helper method to obtain IP of our router
def get_default_gateway_linux():
    return scapy.conf.route.route("0.0.0.0")[2]


def generate_packets(quantity=1, address=None):
    """Handler function to create our desired packets. Defaults sending to default gateway address"""
    if (address is None):
        address = get_default_gateway_linux()
    # packets = []
    """Initial testing plan: send off """
    dummy_data = "asdfg"*1000 + " endpacket"
    try:
        for i in range(quantity):
            scapy.send(scapy.IP(dst=str("1.1.1.1"))/scapy.TCP()/dummy_data)
            # scapy.sendp("I'm travelling on python")
    except socket.gaierror as e:
        LOGGER.debug(f"Network error: {e}")


def generate_end_of_transmission():
    scapy.sendp("End Transmission")


def create_session(host, port):
    s = socket.socket()
    LOGGER.debug(f"Attempting connection to: {host}:{port}.")
    try:
        s.connect((host, port))
    except socket.gaierror as e:
        LOGGER.debug(f"Network error: {e}")
    return s


def send_file(s, path):
    with open(path, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)

            if not bytes_read:
                break

            s.sendall(bytes_read)

        LOGGER.info(f"File at {path} sent.")


def handler(only_logger=False):
    LOGGER.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    LOGGER.addHandler(handler)

    if only_logger:
        return

    s = create_session(DESTINATION_HOST, DESTINATION_PORT)
    LOGGER.info("Session created.")
    send_file(s, DATA_FILE_PATH)
