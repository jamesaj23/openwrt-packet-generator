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

LOGGER = logging.getLogger()

class Coordinator():
    """Coordinator to launch iperf measurements and gather results"""
    def __init__(self, id, config):
        self.id = id
        self.config = config

    def _generate_connections(self):
        """
        Generate required socket objects SEQUENTIALLY
        :return: dict of sensor names and their relevant connection
        """
        pass

    def _generate_clients(self):
        """
        Spin up a thread for each required client, launch iperf instance

        Since we are creating processes via subprocess, this can be handled
        only in threads with little performance cost.

        :param client_config: Slice of config dict containing the clients
        :return: List of outputs from each client
        """
        threads = []
        results = [None for i in range(len(self.config["clients"]))]
        print(f"Len results: {len(results)}")
        for idx, client in enumerate(self.config["clients"]):
            client_args = [
                idx,
                results,
                client["port"],
                client["interval"],
                client["host"],
                client["delay"],
                client["tos"],
                client["iperf_timeout"]
            ]
            LOGGER.info(f"Client args for client {idx}: {client_args}")
            thread = threading.Thread(
                target=ipt.start_client,
                args=client_args
            )
            threads.append(thread)

        # Start all threads
        for th in threads:
            th.start()

        # Wait until all threads have completed
        for idx, th in enumerate(threads):
            try:
                th.join()
            except Exception as e:
                LOGGER.debug(e)
                # Record failure in the results list
                results[idx] = str(e)

        return results

    def _format_result(self, result):
        """
        Format a single JSON test output into a dict, then tabulate
        :param str result: String of iperf3 shell output,
         JSON-formatted if test ran correctly
        :return: pandas DataFrame of test output
        """
        try:
            result_dict = json.loads(result)
        except json.decoder.JSONDecodeError as e:
            return e

        df = pd.DataFrame(
            columns=[
                "start_time",
                "end_time",
                "duration",
                "num_bytes",
                "bits_per_second",
                "omitted",
            ]
        )

        for interval in result_dict["intervals"]:
            df = df.append({
                "start_time": interval["sum"]["start"],
                "end_time": interval["sum"]["end"],
                "duration": interval["sum"]["seconds"],
                "num_bytes": interval["sum"]["bytes"],
                "bits_per_second": interval["sum"]["bits_per_second"],
                "omitted": interval["sum"]["omitted"],
            }, ignore_index=True)

        return df

    def _collect_results(self, results):
        """
        Collect and save results for all tests
        """
        pass

    def run_experiment(self):
        results = self._generate_clients()
        formatted_results = []
        for r in results:
            formatted_results.append(self._format_result(r.stdout))

        return formatted_results
