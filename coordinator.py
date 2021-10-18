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

    def _generate_clients(self, client_config):
        """
        Spin up a thread for each required client, launch iperf instance
        :param client_config: Slice of config dict containing the clients
        :return: List of outputs from each client
        """
        threads = []
        results = []
        for client in client_config:
            client_args = ""
            thread = threading.Thread(
                target=ipt.start_client,
                args=[client_args]
            )
            threads.append(thread)

        # Start all threads
        for th in threads:
            th.start()

        # Wait until all threads have completed
        for th in threads:
            th.join()

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
            return result_dict
        except json.decoder.JSONDecodeError as e:
            return e

    def _collect_results(self, results):
        """
        Collect and save results for all tests
        """
        pass

    def run_experiment(self):
        results = self._generate_clients()
        formatted_results = []
        for r in results:
            formatted_results.append(self._format_result(r))
        self._collect_results(formatted_results)
