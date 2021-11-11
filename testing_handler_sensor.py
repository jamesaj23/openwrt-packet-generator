import logging
import sys

import iperf_tools as ipt
import connections as conn
import sensor
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
LOGGER.addHandler(handler)


def start_server(port):
    result = ipt.start_server(port)
    return result


def start_sensor(coordinator_host, port, delay=0, csv_tag=None):
    se = sensor.Sensor(0, coordinator_host, port, delay, csv_tag)
    return se.run_experiment()


def start_server_loop(port):
    while True:
        ipt.start_server(port)


def test_connection(host, port, payload):
    LOGGER.info(f"Attempting to establish connection at: {host}, {port}")
    s = conn.establish_client_connection(host, port)
    LOGGER.info(f"Attempting to send payload")
    conn.send_payload(s, payload)
    return
