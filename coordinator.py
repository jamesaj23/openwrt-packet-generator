import socket
import logging
import sys
import time
import asyncio

import iperf3
import numpy as np
import pandas as pd


class Coordinator():
    """Coordinator to launch iperf measurements and gather results"""
    def __init__(self, id, config):
        self.id = id
        self.config = config

    def generate_connections():
        """
        Generate required socket objects SEQUENTIALLY
        :return: dict of sensor names and their relevant connection
        """
        pass