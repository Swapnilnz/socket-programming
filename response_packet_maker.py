"""Functions in this file are responsible for making DT-Response Packets.
   The contents of the packets are described in the assignment and are 
   dependent on whether the date is request or the time (and also which language).
   
   Author: Swapnil Bhagat
   Date: 12th August 2020
   
   COSC264 Assignment 2
"""

import datetime


def make_time_text_bytearray(language, hour, minute):
    """Makes and returns the bytearray object containing 
    the required utf-8 encoded message (time in hours:minutes) 
    in the given language parameter.
    """
    # Create time response depending on language
    response_text = ""
    if language == "English":
        response_text = "The current time is {0:0=2d}:{1:0=2d}".format(hour, minute)
    elif language == "Maori":
        response_text = "Ko te wa o tenei wa {0:0=2d}:{1:0=2d}".format(hour, minute)
    elif language == "German":
        response_text = "Die Uhrzeit ist {0:0=2d}:{1:0=2d}".format(hour, minute)

    # Encode string into bytearray
    text_bytearray = response_text.encode('utf-8')
    return text_bytearray


def make_date_text_bytearray(language, month_dic, day, month, year):
    """Makes and returns the bytearray object containing 
    the required utf-8 encoded message (date in day, month, year or similar) 
    in the given language parameter. The MONTH_DIC dictionary is used 
    for the textual months in the three languages.
    """
    # Constants used to index language in the MONTH_DIC - makes code more readable
    english = 0
    maori = 1
    german = 2

    # Create date response depending on language
    response_text = ""
    if language == "English":
        response_text = "Today's date is {} {}, {}".format(month_dic[int(month)][english], day, year)
    elif language == "Maori":
        response_text = "Ko te ra o tenei ra ko {} {}, {}".format(month_dic[int(month)][maori], day, year)
    elif language == "German":
        response_text = "Heute is der {} {}, {}".format(month_dic[int(month)][german], day, year)

    # Encode string into bytearray
    text_bytearray = response_text.encode('utf-8')
    return text_bytearray


def make_constant_list(language):
    """Makes/returns list of constants to be used in packet header (these were defined in the assignment).
       Namely: Magic Number, Packet Type, and Language Code
    """
    # Magic number, packet type, and language code constants (language is dependent on port)
    magic_no = [0x49, 0x7E]
    packet_type = [0x00, 0x02]
    request_type = []
    if language == "English":
        request_type = [0x00, 0x01]
    elif language == "Maori":
        request_type = [0x00, 0x02]
    elif language == "German":
        request_type = [0x00, 0x03]

    constant_list = magic_no + packet_type + request_type
    return constant_list


def make_response_packet(language, month_dic, request_type):
    """Receives an either date or time request (dateOrTimeRequest)
       and creates a DT-Response packet using the current date and time
       (provided by the datetime library). Returns a complete packet bytearray
       with all required packet information.
    """
    # Get date and time as an integer
    day = int(datetime.datetime.today().strftime('%d'))
    month = int(datetime.datetime.today().strftime('%m'))
    year = int(datetime.datetime.today().strftime('%Y'))
    hour = int(datetime.datetime.now().strftime("%H"))
    minute = int(datetime.datetime.now().strftime("%M"))

    constant_list = make_constant_list(language)

    # Prepare date and time for bytearray
    split_year = [(year >> 8) & 0xff, year & 0xff]
    date_and_time = split_year + [month] + [day] + [hour] + [minute]

    # Make either date or time text bytearray using help functions
    if request_type == 1:
        text = make_date_text_bytearray(language, month_dic, day, month, year)
    elif request_type == 2:
        text = make_time_text_bytearray(language, hour, minute)

    # Calculates length of text for 'length' element of packet
    # returns None if packet is too long so that while loop starts again
    length = [len(text)]
    if not (length[0] <= 255):
        print("Response text is too long, unable to send!")
        return None

    # Last step: create packet by creating packet header bytearray then adding the text bytearray
    packet_header = constant_list + date_and_time + length
    packet = bytearray(packet_header) + text

    return packet
