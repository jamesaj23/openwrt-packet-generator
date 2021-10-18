import socket
import logging
import sys
import time
import asyncio
import json
import threading

import iperf3
import numpy as np
import pandas as pd

import iperf_tools as ipt


class Sensor():
    """Sensor to launch iperf measurement and gather result"""
    def __init__(self, id, config):
        self.id = id
        self.config = config

    def generate_server(self):
        ipt.start_server()

    def format_result():
        pass

    def run_experiment():
        pass