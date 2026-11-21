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
        len_field = b''
        while len(len_field) < 4:
            received_payload = conn.recv(4 - len(len_field))

            if len(received_payload) == 0:
                # Close server
                print("Failed fully reading a received message")
                conn.close()
                continue

            len_field += received_payload

        message_length = struct.unpack("<i", len_field)[0]

        # Retrieve the message data
        data_field = b''
        while len(data_field) < message_length:
            received_payload = conn.recv(message_length - len(data_field))

            if len(received_payload) == 0:
                # Close server
                print("Failed fully reading a received message")
                conn.close()
                continue

            data_field += received_payload

        message_data = data_field.decode("utf-8")

        # Print the message received
        print(f"Received data: {message_data}")

        conn.close()


def get_args() -> argparse.Namespace:
    """
    Parse the program arguments: server IP, server port
    """
    parser = argparse.ArgumentParser(description="Listen to incoming server connections.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    return parser.parse_args()


def main() -> int:
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
