import socket
import logging
import sys
import time
import asyncio

import subprocess
import iperf3
import numpy as np
import pandas as pd


LOGGER = logging.getLogger()


def start_client(index, results, port, interval, host, delay, tos, iperf_timeout):
    """
    Launch iperf client session through a subproccess.
    This offloads most of the parallelism away from python as,
    well as enabling the use of the iperf TOS/DSCP fields,
    which are not presently supported in the iperf3 python library.
    """
    LOGGER.info(f"Starting client at idx: {index}")
    shell_statement = [
                "iperf3",
                # GENERAL OPTIONS
                "--port", port,
                "--format", "k",
                "--interval", interval,
                "--json",
                # CLIENT SPECIFIC OPTIONS
                "--client", host,
                "--verbose",
                "--time", delay,
                "--reverse",  # Client receives, server sends
                "--tos", tos,  # TOS/DSCP vector
            ]
    LOGGER.info(f"Shell statement: {shell_statement}")
    # try:
    iperf_out = subprocess.run(
        shell_statement,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=iperf_timeout,
        universal_newlines=True,
    )
    results[index] = iperf_out
    LOGGER.info(iperf_out)
    return iperf_out
    # except subprocess.TimeoutExpired:
    #     return iperf_shell_error("iperf-timeout", traceback=None)


def iperf_shell_error(key, traceback=None):
    return "Error!!!!"


def start_server(port):
    """
    Launch an iperf server session through the python iperf3 libary.
    The server doesn't care about parallelism, and TOS/DSCP should
    only need to be specified on the client end.
    """
    server = iperf3.Server()
    server.port = port
    server.verbose = True
    result = server.run()
    return result
    
