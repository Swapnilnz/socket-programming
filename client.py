""" Client side of client-server relationship.
    Requests date or time from server and checks the incoming packet for validity.
    
    Author: Swapnil Bhagat
    Date: 12th August 2020
    
    COSC264 Assignment 2
"""

import sys
import socket
import select
import packet_checker

# Constants 
BUFFER_SIZE = 1024


def pretty_printer(packet, text):
    """Responsible for simply printing the received DT-Response packet in a more readable manner.
    """
    languages = ["English", "Te Reo Maori", "German"]
    magic_number, request_type, language_code, year, month, day, hour, minute, length = packet
    try:
        width = 50
        print("-" * width)
        print("Packet Header Contents".center(50))
        print("-" * width)
        print("Magic number: {}".format(magic_number))
        print("Packet type: {} (DT-Response Packet)".format(request_type))
        print("Language code: {} ({})".format(language_code, languages[language_code - 1]))
        print("Date: {0:0=2d}/{1:0=2d}, {2}".format(day, month, year))
        print("Time: {0:0=2d}:{1:0=2d}".format(hour, minute))
        print("Packet length: {} bytes".format(length))
        print("-" * width)
        print("Message From Server".center(width))
        print("-" * width)
        print(text.center(width))
        print("-" * width)
    except:
        raise Exception("Could not print message!")


def make_request_packet(request_type):
    """Creates the DT-Request Packet as outlined in the assignment.
       Contents: Magic Number, Packet Type, and the date or time code
    """
    # Some constants from assignment
    magic_num = [0x49, 0x7E]
    packet_type = [0x00, 0x01]
    # Make the contents of hex values for packet
    packet_content_list = magic_num + packet_type + request_type
    byte_array = bytearray(packet_content_list)
    return byte_array


def input_check(argv):
    """Checks the command line input arguments for validity.
    """
    # Check date or time is correct (has to be 'date' or 'time')
    date_or_time = argv[1]
    date_literal = "date"
    time_literal = "time"
    if date_or_time == date_literal:
        request_type = [0x00, 0x01]
    elif date_or_time == time_literal:
        request_type = [0x00, 0x02]
    else:
        raise SyntaxError("Please enter either 'date' or 'time' for your request!")

    # Check valid input address
    input_address = argv[2]
    try:
        ip_address = socket.gethostbyname(input_address)
    except:
        raise SyntaxError("Please enter a valid host name or dotted decimal notion IP address.")

    # Check valid port number (between 1024 and 64000 inclusive)
    input_port_number = int(argv[3])
    try:
        if (input_port_number >= 1024) and (input_port_number <= 64000):
            port_num = input_port_number
        else:
            raise SyntaxError("Please enter a valid port number (between 1024 and 64000)!")
    except:
        raise SyntaxError("Please enter a valid port number (between 1024 and 64000)!")

    return request_type, ip_address, port_num


def main():
    """Responsible for controlling the flow of the logic through calling helper functions
       int the right order. After the client UDP socket is created, it sends a 
       DT-Request packet to the server. It listens for exactly one second for 
       a response from the server, after which the DT-Response packet is checked and printed.
    """
    # Check input data
    request_type, ip_address, port_num = input_check(sys.argv)

    # Create socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        raise Exception("Unable to create a client socket!")

    # Make request packet according to dateOrTimeCode entered (date or time)
    request_packet = make_request_packet(request_type)

    # Send data to socket
    full_address = (ip_address, port_num)
    try:
        client_socket.sendto(request_packet, full_address)
    except:
        client_socket.close()
        raise Exception("Could not send request packet!")

    # Get response in one second
    timeout = 5
    read_sockets, write_sockets, error = select.select([client_socket], [], [], timeout)

    # Get contents from socket
    if len(read_sockets) != 0:
        packet_header_len = 13
        received_message, address = client_socket.recvfrom(BUFFER_SIZE)
        checked_packet_contents = packet_checker.response_packet_check(received_message)
        text = received_message[packet_header_len:].decode('utf-8')
        if checked_packet_contents is not None:
            pretty_printer(checked_packet_contents, text)
        else:
            client_socket.close()
            raise Exception("Packet contents are not well formed!")

    else:
        # No response in one second
        client_socket.close()
        raise Exception("Connection timed out: did not receive response packet in {} second(s)!".format(timeout))


main()
