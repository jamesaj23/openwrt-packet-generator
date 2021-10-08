import socket
import logging
import sys
import time
import asyncio

import subprocess
import iperf3
import numpy as np
import pandas as pd


def begin_iperf_client(port):
    """
    Launch iperf client session through a subproccess.
    This offloads most of the parallelism away from python as,
    well as enabling the use of the iperf TOS/DSCP fields,
    which are not presently supported in the iperf3 python library.
    """
    try:
        iperf_out = subprocess.run(
            [
                "iperf3",
                # GENERAL OPTIONS
                "--port", port,
                "--format", "k",
                "--interval", interval,
                "--client",
                "--json",
                # CLIENT SPECIFIC OPTIONS
                "--client", host,
                "--time", time,
                "--reverse",  # Client receives, server sends
                "--tos", tos,  # TOS/DSCP vector
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=iperf_timeout,
            universal_newlines=True,
        )
        except subprocess.TimeoutExpired:
            return self._get_wget_error("wget-timeout", url, traceback=None)
    pass


def begin_iperf_server():
    """
    Launch an iperf server session through the python iperf3 libary.
    The server doesn't care about parallelism, and TOS/DSCP should
    only need to be specified on the client end.
    """
    server = iperf3.Server()
    server.port = port
    server.verbose = True
