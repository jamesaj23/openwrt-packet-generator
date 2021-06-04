import iperf3


def run_client():
    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = '127.0.0.1'
    result = client.run()
    return result


def run_server():
    server = iperf3.Server()
    result = server.run()
    return result
