"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import pmt
import numpy as np
from gnuradio import gr

from datetime import datetime



class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, format_timestamp=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Print DroneID Packets',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.format_timestamp = int(format_timestamp)
        self.message_port_register_in(gr.pmt.intern("in"))
        self.set_msg_handler(gr.pmt.intern("in"), self.handle_msg)
        self.id = 0
        
    def handle_msg(self, msg):
        msg = pmt.to_python(msg)
        try:
            mac_tx = [msg[0]['address 2'], msg[0]['address 1'], msg[0]['address 3']]
            if "e8:94:f6:09:ae:bd" in mac_tx:
                if self.format_timestamp == 1:
                    timestamp = msg[0]['wifi_toa']
                    seconds = int(timestamp)  # Extract seconds
                    nanoseconds = int((timestamp - seconds) * 1e9)  # Extract nanoseconds

                    formatted_time = f"{datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')}.{nanoseconds:09d}"

                    print(f"[{self.id}] DroneID Packet found: {formatted_time} - {msg[1]} {mac_tx}")
                else:
                    print (f"[{self.id}] DroneID Packet found: {msg[0]['wifi_toa']:.9f} - {msg[1]} {mac_tx}")
            self.id = self.id + 1
        except:
            pass
