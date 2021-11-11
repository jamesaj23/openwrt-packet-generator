import socket
import logging
import sys
import time

import iperf3
import numpy as np
import pandas as pd

LOGGER = logging.getLogger()
LISTEN_DURATION = 5
BUFFER_SIZE = 4096
CODE_SIZE_BYTES = 8

SERVER_HOST = "0.0.0.0"


# Dict of addresses for all hosts
# THIS SHOULD GO IN THE COORDINATOR CLASS
HOST_ADDRESSES = {}
SAMPLE_CONFIG = {
    "host": "",
    "client": "",
    "duration": "",
    "protocol": "UDP",
    "reverse": "",
    "start_bandwidth": "",
    "end_bandwidth": "",
    "desired_cols": [],
    "to_csv": True,
}


def establish_client_connection(host, port):
    """
    For the purposes of this connection the SENSOR is the CLIENT (sender)
    :param str host: hostname of the SENSOR
    :param int port: desired port of the sensor connection
    :return: Connected socket object
    :rtype: socket.Socket ????
    """
    s = socket.socket()
    LOGGER.debug(f"Attempting connection to: {host}:{port}.")
    try:
        s.connect((host, port))
    except socket.gaierror as e:
        LOGGER.debug(f"Network error: {e}")
    return s


def establish_server_connection(host, port):
    """
    For the purposes of this connection the COORDINATOR is the SERVER (reciever)
    :param str host: hostname of the SENSOR
    :param str port: desired port of the sensor connection
    :return: Tuple of (socket, client_socket, address)
    """
    s = socket.socket()
    s.bind((SERVER_HOST, port))

    s.listen(LISTEN_DURATION)
    client_socket, address = s.accept()
    LOGGER.info(f"Connection accepted at: {address}")
    return client_socket


def send_payload(s, payload):
    LOGGER.info("Sending payload.")
    s.sendall(payload.encode())
    LOGGER.info("Payload sent.")


def receive_payload(client_socket):
    bytes_read = None
    while True:
        # payload = ""
        bytes_read = client_socket.recv(BUFFER_SIZE).decode()
        if not bytes_read:
            break
    return bytes_read


def coordinator_handshake(client_socket, code=None):
    """
    Verify that the connection is still live,
    optionally check sync with a code
    Coordinator receives message from test sensor
    :param socket.socket s: Existing socket over which the connection exists
    :param int code: Number to verify that both clients are in sync  
    :return: Boolean if code was correct
    """
    try:
        time.sleep(0.5)
        client_socket.recv(CODE_SIZE_BYTES)
    except Exception as e:
        raise e

    return True


def sensor_handshake(s, code=None):
    """
    Verify that the connection is still live,
    optionally check sync with a code
    Sensor sends message to coordinator
    Note that the host WILL NOT be notified if the sent code is wrong

    :param socket.socket s: Existing socket over which the connection exists
    :param int code: Number to verify that both clients are in sync
    :return: Boolean if code was correct

    """
    try:
        time.sleep(0.5)
        s.sendall(code)
    except Exception as e:
        raise e
    return True
