import socket
import struct
import pmt
import time
import numpy as np
from gnuradio import gr

class UDPTagSender(gr.basic_block):
    def __init__(self, udp_ip="127.0.0.1", udp_port=5005):
        gr.basic_block.__init__(self,
            name="UDP Tag Sender",
            in_sig=[(np.complex64, 1)],  # Assuming complex samples
            out_sig=None)
        
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mac_address = "00:11:22:33:44:55"  # Replace with actual MAC

    def general_work(self, input_items, output_items):
        nread = self.nitems_read(0)  # Get the starting sample index
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tags:
            key = pmt.to_python(tag.key) # convert from PMT to python string
            value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was
            print(f"key: {key}")
            print(f"value: {value} as {type(value)}")
             
        timestamp = time.time()  # Dummy timestamp (current time)
        mac_address = bytes.fromhex("001122334455")  # Dummy MAC address (6 bytes)
        
        packet_data = struct.pack("!d6s", timestamp, mac_address)  # 8 bytes timestamp + 6 bytes MAC
        
        self.sock.sendto(packet_data, (self.udp_ip, self.udp_port))

        self.consume(0, len(input_items[0]))  # Consume all samples
        return 0
