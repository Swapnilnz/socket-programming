# socket-programming
Python socket programming (network architecture)

The project goal was to create a client that sends a current date or time request to a server, which replies by giving both and also a customised message 
in either Te Reo Maori, English, or German.

To set up, run the server application through the command line with three arguments, each being a port number (1024 >= portnum <= 64000). These port numbers
represent English, Te Reo Maori, and German respectively. For example, in cmd: "python server.py 12000 12001 12002"
Subsequently, to request a date/time, run the client application in cmd via: "python client.py date|time 12000|12001|12002"
The port number chosen will dictate the language of the message.

