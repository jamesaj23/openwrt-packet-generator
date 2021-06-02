"""File to be run on the device receiving transmission"""

import socket
import os
import logging

import tqdm

from packet_gen import BUFFER_SIZE


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

LOGGER = logging.getLogger()


def create_session(host, port):
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))

    s.listen(5)
    client_socket, address = s.accept()
    LOGGER.info(f"Connection accepted at: {client_socket}, {address}.")


def receive_bytes(s, client_socket, address):
    """We don't actually care about the file, no need to write anywhere"""
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            break
