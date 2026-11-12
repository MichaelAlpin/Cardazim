"""
The code responsible for running the server and getting data from clients
"""

import argparse
import socket
import struct
import sys


def run_server(ip: str, port: int) -> None:
    """
    Listen to incoming connections on the given address
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen()

    while True:
        conn, _ = server_sock.accept()

        # Retrieve the message length
        msg_len = bytes([])
        while len(msg_len) < 4:
            received_payload = conn.recv(4 - len(msg_len))

            if len(received_payload) == 0:
                print("Failed fully reading a received message")
                return

            msg_len += received_payload
        msg_len = struct.unpack("<i", msg_len)[0]

        # Retrieve the message data
        msg_data = bytes([])
        while len(msg_data) < msg_len:
            received_payload = conn.recv(msg_len - len(msg_data))

            if len(received_payload) == 0:
                print("Failed fully reading a received message")
                return

            msg_data += received_payload
        msg_data = struct.unpack(f"{msg_len}s", msg_data)[0].decode("utf-8")

        # Print the message received
        print(f"Received data: {msg_data}")


def get_args() -> argparse.Namespace:
    """
    Parse the program arguments: server IP, server port
    """
    parser = argparse.ArgumentParser(description="Listen to incoming server connections.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and starting a server.
    """
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
    except OSError as error:
        print(f"ERROR: {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
