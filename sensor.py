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

class Sensor():
    """Sensor to launch iperf measurement and gather result"""
    def __init__(self, id, coordinator_host, port, csv_tag=None):
        self.id = id
        self.coordinator_host = coordinator_host
        self.port = port
        self.csv_tag = csv_tag

    def generate_server(self):
        return ipt.start_server(self.port)

    def format_result(self, result):
        try:
            result_dict = result.json
        except json.decoder.JSONDecodeError as e:
            return e

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
            ]
        )

        for interval in result_dict["intervals"]:
            df = df.append({
                "start_time": interval["streams"][0]["start"],
                "end_time": interval["streams"][0]["end"],
                "duration": interval["streams"][0]["seconds"],
                "num_bytes": interval["streams"][0]["bytes"],
                "bits_per_second": interval["streams"][0]["bits_per_second"],
                "retransmits": interval["streams"][0]["retransmits"],
                "snd_cwnd": interval["streams"][0]["snd_cwnd"],
                "rtt": interval["streams"][0]["rtt"],
                "rttvar": interval["streams"][0]["rttvar"],
                "pmtu": interval["streams"][0]["pmtu"],
                "omitted": interval["streams"][0]["omitted"],
            }, ignore_index=True)

        return df

    def run_experiment(self):
        time_string = datetime.datetime.now().strftime("%d_%m_%y %H_%M_%S")
        result = self.generate_server()
        formatted_result = self.format_result(result)
        if self.csv_tag is not None:
            fname = f"csvdump/{time_string}_{self.csv_tag}.csv"
            formatted_result.to_csv(fname)
            LOGGER.info(f"Written to file: {fname}")
