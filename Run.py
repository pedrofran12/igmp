#!/usr/bin/env python

from Daemon.Daemon import Daemon
import Main
import _pickle as pickle
import socket
import sys
import os
import argparse
import traceback


def client_socket(data_to_send):
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = './uds_socket'
    #print('connecting to %s' % server_address)
    try:
        sock.connect(server_address)
        sock.sendall(pickle.dumps(data_to_send))
        data_rcv = sock.recv(1024 * 256)
        if data_rcv:
            print(pickle.loads(data_rcv))
    except socket.error:
        pass
    finally:
        #print('closing socket')
        sock.close()


class MyDaemon(Daemon):
    def run(self):
        Main.main()
        server_address = './uds_socket'

        # Make sure the socket does not already exist
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise

        # Create a UDS socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Bind the socket to the port
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)
        while True:
            try:
                connection, client_address = sock.accept()
                data = connection.recv(256 * 1024)
                print(pickle.loads(data))
                args = pickle.loads(data)
                if args.list_interfaces:
                    connection.sendall(pickle.dumps(Main.list_enabled_interfaces()))
                elif args.list_state:
                    connection.sendall(pickle.dumps(Main.list_state()))
                elif args.add_interface:
                    Main.add_interface(args.add_interface[0])
                    connection.shutdown(socket.SHUT_RDWR)
                elif args.remove_interface:
                    Main.remove_interface(args.remove_interface[0])
                    connection.shutdown(socket.SHUT_RDWR)
                elif args.stop:
                    Main.remove_interface("*")
                    connection.shutdown(socket.SHUT_RDWR)
            except Exception:
                connection.shutdown(socket.SHUT_RDWR)
                traceback.print_exc()
            finally:
                # Clean up the connection
                connection.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IGMP')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-start", "--start", action="store_true", default=False, help="Start IGMP")
    group.add_argument("-stop", "--stop", action="store_true", default=False, help="Stop IGMP")
    group.add_argument("-restart", "--restart", action="store_true", default=False, help="Restart IGMP")
    group.add_argument("-li", "--list_interfaces", action="store_true", default=False, help="List All IGMP Interfaces")
    group.add_argument("-ls", "--list_state", action="store_true", default=False, help="List state")
    group.add_argument("-ai", "--add_interface", nargs=1, metavar='INTERFACE_NAME', help="Add IGMP interface")
    group.add_argument("-ri", "--remove_interface", nargs=1, metavar='INTERFACE_NAME', help="Remove IGMP interface")
    group.add_argument("-v", "--verbose", action="store_true", default=False, help="Verbose (print all debug messages)")
    args = parser.parse_args()

    daemon = MyDaemon('/tmp/Daemon-igmp.pid')
    if args.start:
        print("start")
        daemon.start()
        sys.exit(0)
    elif args.stop:
        client_socket(args)
        daemon.stop()
        sys.exit(0)
    elif args.restart:
        daemon.restart()
        sys.exit(0)
    elif args.verbose:
        os.system("tailf stdout")
        sys.exit(0)
    elif not daemon.is_running():
        print("IGMP is not running")
        parser.print_usage()
        sys.exit(0)

    client_socket(args)
