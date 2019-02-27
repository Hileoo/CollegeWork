#!/usr/bin/python
# -*- coding: UTF-8 -*-

from socket import *


def handle_request(tcp_socket):

    # Receive request message from the client on connection socket
    message = tcp_socket.recv(1024)

    # Extract the path of the requested object from the message (second part of the HTTP header)
    filename = message.split()[1]

    try:
        # Read the corresponding file from disk
        f = open(filename[1:])  # Read from the second character to split the '/' in filename

    except IOError:
        # When a requested file is not available on the server, return a response with the status code 404 NOT FOUND
        tcp_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n<html><body>404 Not Found</body></html>')

    else:
        output_data = f.read()
        # Send the HTTP response header line to the connection socket
        tcp_socket.send(b'HTTP/1.1 200 OK\r\n\r\n')
        # Send the content of the file to the socket
        tcp_socket.send(output_data.encode())

    # Close the connection socket
    tcp_socket.close()


def start_server(server_address, server_port):
    # Create server socket
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Bind the server socket to server address and server port
    server_socket.bind((server_address, server_port))

    # Continuously listen for connections to server socket
    server_socket.listen(1)

    while True:
        print("Ready to serve......")
        # Set up a new connection from the client
        connection_socket, addr = server_socket.accept()

        # Call the function
        handle_request(connection_socket)

    # Close server socket
    server_socket.close()


start_server("", 8000)
# Note: my IP address: 10.129.22.210   WLAN: web.wlan.bjtu
