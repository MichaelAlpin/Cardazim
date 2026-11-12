"""
The code responsible for sending messages to the server
"""

import argparse
import socket
import struct
import sys


def send_data(server_ip: str, server_port: int, data: str) -> None:
    """
    Send data to server in address (server_ip, server_port).
    """
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((server_ip, server_port))
    print("Sending message...")
    encoded_data = data.encode("utf-8")
    client_sock.sendall(struct.pack(f"<i{len(encoded_data)}s", len(encoded_data), encoded_data))
    client_sock.close()


def get_args() -> argparse.Namespace:
    """
    Parse the program arguments: server IP, server port, data
    """
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("data", type=str, help="the data")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print("Done.")
    except OSError as error:
        print(f"ERROR: {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
