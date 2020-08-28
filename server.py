"""Server-side application of client-server relationship.
   Takes three port numbers in the command line arguments and opens three 
   sockets (using the Socket API), each relating to a respective language: English, Te Reo Maori, and German. 
   Depending on which of these three sockets the client and connected with,
   the date or time (chosen again by the user) will be sent in the corresponding language.
   
   Author: Swapnil Bhagat
   Date: 12th August 2020
   
   COSC264 Assignment 2
"""

import sys
import socket
import select
import packet_checker
import response_packet_maker

# Constants
DATE_REQUEST = 1
TIME_REQUEST = 2
BUFFER_SIZE = 1024
MONTH_DICTIONARY = {1: ["January", "Kohitatea", "Januar"],
                    2: ["Febuary", "Hui-tanguru", "Februar"],
                    3: ["March", "Poutu-te-rangi", "Marz"],
                    4: ["April", "Paenga-whawha", "April"],
                    5: ["May", "Haratua", "Mai"],
                    6: ["June", "Pipiri", "Juni"],
                    7: ["July", "Hongongoi", "Juli"],
                    8: ["September", "Here-turi-koka", "August"],
                    9: ["October", "Mahuru", "September"],
                    10: ["October", "Whiringa-a-nuku", "Oktober"],
                    11: ["November", "Whiringa-a-rangi", "November"],
                    12: ["December", "Hakihea", "Dezember"]}


def listen(socket_list):
    """Perpetually listens for incoming DT-Requests until one is received.
       Packet is then checked, processed, then a DT-Response packet is sent
    """
    while True:
        # Checks if any socket from socketList has received a packet.
        # It is assumed only one socket will be sent a packet.
        read_sockets, write_sockets, error = select.select(socket_list, [], [])
        received_on_socket = read_sockets[0]

        # Gets packet contents and address
        received_bytes, received_address = received_on_socket.recvfrom(BUFFER_SIZE)
        received_byte_array = bytearray(received_bytes)

        # Determines which socket received the packet and hence which language is requested
        languages = ["English", "Maori", "German"]
        language = None
        for i in range(len(socket_list)):
            if received_on_socket == socket_list[i]:
                language = languages[i]

        # Check packet contents for validity. If valid check if date or time is requested
        request_type = packet_checker.request_packet_check(received_byte_array)
        if request_type:
            response_packet = response_packet_maker.make_response_packet(language, MONTH_DICTIONARY, request_type)
            if response_packet is not None:
                return response_packet, received_on_socket, received_address
        else:
            print("Packet was not well formed as a DT-Request Packet")


def create_sockets(english_port, maori_port, german_port):
    """Create three sockets, one for the English language, one for Te Reo Maori, and one for German.
       The client connects to the port (each bound to one socket) corresponding to their required language. 
    """
    # Local host IP (as outline by the Socket API)
    host_ip = ''
    # Use Socket API to create socket; appropriate error message if it fails is shown
    try:
        english_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        maori_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        german_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        raise Exception("Failed to create one or more sockets")
    # Binds each socket to a command line argument given port
    try:
        english_socket.bind((host_ip, english_port))
        maori_socket.bind((host_ip, maori_port))
        german_socket.bind((host_ip, german_port))
    except:
        raise Exception("Failed to bind one or more sockets")

    return english_socket, maori_socket, german_socket


def port_num_check(argv):
    """Checks the three input arguments (port numbers) to be valid.
       This means they all must be different and between 1024 and 64000 (inclusive).
    """
    # Checks if any arguments are identical, or too many arguments are given 
    # Note: the file name is automatically an argument so is account for 
    if len(set(argv)) != 4:
        raise Exception("Please enter three different port numbers")
    return_tup = tuple()

    # Checks port numbers are in range, showing exception errors if not
    try:
        for num in argv[1:]:
            if (int(num) >= 1024) and (int(num) <= 64000):
                return_tup += (int(num),)
            else:
                raise Exception("Port number {} is not within range 1024 and 64000".format(str(num)))
    except:
        raise Exception("Please enter three valid port number integers")

    return return_tup


def main():
    """The main method is responsible for controlling the logic 
       through calling helper functions in the right order.
       The UDP sockets are created then bound to a port; they then listen 
       for any DT-Request packets, and after receiving process the packets and form
       and send a DT-Response packet.
    """

    # Check command line argument port numbers
    try:
        english_port, maori_port, german_port = port_num_check(sys.argv)
    except:
        raise Exception("Could not get command line arguments from sys!")

    # Create and bind sockets from port numbers: English, Maori, German (in that order)
    english_socket, maori_socket, german_socket = create_sockets(english_port, maori_port, german_port)
    socket_list = [english_socket, maori_socket, german_socket]

    # Listen for incoming packets then process
    response_packet, received_on_socket, received_address = listen(socket_list)

    # Send response packet
    try:
        received_on_socket.sendto(response_packet, received_address)
    except:
        raise Exception("Could not send response packet using sendto()!")

    # Return sockets to operating system
    for sock in socket_list:
        sock.close()
    print("Connection closing...")
    sys.exit()


main()
