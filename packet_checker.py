"""Functions in this file are responsible for checking DT-Request/Response Packets
   for validity. Validity is defined in the assignment document. 
   
   Author: Swapnil Bhagat
   Date: 12th August 2020
   
   COSC264 Assignment 2
"""


def response_packet_check(packet):
    """Check the DT-Response packet for validity.
       Returns all the components of the packet header.
    """
    if len(packet) < 13:
        print("Received message is too short!")
        return None
    received_magic_no = (packet[0] << 8) | packet[1]
    if received_magic_no != 0x497E:
        print("Received magic number is incorrect!")
        return None
    received_packet_type = (packet[2] << 8) | packet[3]
    if not (received_packet_type == 2):
        print("Received packet type is incorrect!")
        return None
    received_request_type = (packet[4] << 8) | packet[5]
    if received_request_type not in [1, 2, 3]:
        print("Received language code is incorrect!")
        return None
    year = int(hex((packet[6] << 8) | packet[7]), 16)
    if year >= 2100:
        print("Year is too high!")
        return None
    month = packet[8]
    if not (1 <= month <= 12):
        print("Month is not between 1 and 12!")
        return None
    day = packet[9]
    if not (1 <= day <= 31):
        print("Day is not between 1 and 31!")
        return None
    hour = packet[10]
    if not (0 <= hour <= 23):
        print("Hour is not between 0 and 23!")
        return None
    minute = packet[11]
    if not (0 <= minute <= 59):
        print("Minute is not between 0 and 59!")
        return None
    length = packet[12]
    if not (13 + length == len(packet)):
        print("Message length is inaccurate!")
        return None
    return received_magic_no, received_packet_type, received_request_type, year, month, day, hour, minute, length


def request_packet_check(packet):
    """Check the DT-Request packet for validity.
       Returns 0 if invalid, 1 if date is requested, or 2 if time is requested. 
    """
    split_magic_no = 0x497E
    split_packet_type = 0x0001
    split_date = 0x0001
    split_time = 0x0002
    if len(packet) != 6:
        return 0
    magic_no = (packet[0] << 8) | packet[1]
    if magic_no != split_magic_no:
        return 0
    packet_type = (packet[2] << 8) | packet[3]
    if packet_type != split_packet_type:
        return 0
    request_type = (packet[4] << 8) | packet[5]
    if request_type == split_date:
        return 1
    elif request_type == split_time:
        return 2
    else:
        return 0
