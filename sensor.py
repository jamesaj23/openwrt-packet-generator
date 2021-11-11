import socket
import logging
import sys
import time
import asyncio
import json
import threading
import datetime

import iperf3
import numpy as np
import pandas as pd

import iperf_tools as ipt
import connections as conn

LOGGER = logging.getLogger()
REPORTING_INTERVAL = "0.25"


class Sensor():
    """Sensor to launch iperf measurement and gather result"""
    def __init__(self, id, coordinator_host, port, delay=0, csv_tag=None, iperf_timout=180):
        self.id = id
        self.coordinator_host = coordinator_host
        self.port = port
        self.csv_tag = csv_tag
        self.delay = delay
        self.iperf_timout = iperf_timout

    def generate_server(self):
        return ipt.start_server(self.port, REPORTING_INTERVAL, self.iperf_timout)

    def format_result(self, result):
        try:
            result_dict = json.loads(result)
        except json.JSONDecodeError as e:
            LOGGER.debug(e)
            raise e

        df = pd.DataFrame(
            columns=[
                "start_time",
                "end_time",
                "duration",
                "num_bytes",
                "bits_per_second",
                "retransmits",
                "snd_cwnd",
                "rtt",
                "rttvar",
                "pmtu",
                "omitted",
                "delay",
            ]
        )

        for interval in result_dict["intervals"]:
            df = df.append({
                "start_time": float(interval["streams"][0]["start"]) + self.delay,
                "end_time": float(interval["streams"][0]["end"]) + self.delay,
                "duration": interval["streams"][0]["seconds"],
                "num_bytes": interval["streams"][0]["bytes"],
                "bits_per_second": interval["streams"][0]["bits_per_second"],
                "retransmits": interval["streams"][0]["retransmits"],
                "snd_cwnd": interval["streams"][0]["snd_cwnd"],
                "rtt": interval["streams"][0]["rtt"],
                "rttvar": interval["streams"][0]["rttvar"],
                "pmtu": interval["streams"][0]["pmtu"],
                "omitted": interval["streams"][0]["omitted"],
                "delay": self.delay,
            }, ignore_index=True)

        return df

    def run_experiment(self):
        time_string = datetime.datetime.now().strftime("%d_%m_%y %H_%M_%S")
        result = self.generate_server()
        LOGGER.info("Received results, formatting.")
        formatted_result = self.format_result(result.stdout)
        folder = "wed"
        if self.csv_tag is not None:
            fname = f"csvdump/{folder}/{self.csv_tag}.csv"
            formatted_result.to_csv(fname)
            LOGGER.info(f"Written to file: {fname}")
