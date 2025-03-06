import socket
import pmt
import datetime
from gnuradio import gr

msg_template_dict = {"node": "", "wifi_toa": 0.0, "address 3": "", "address 2": "", "address 1": "", "sequence number": "", "ssid": "", "subtype": "", "type": "", "duration": "", "dlt": "", "frame bytes": "", "encoding": "", "snr": "", "nominal frequency": "", "frequency offset": "", "beta": "", "csi": []}


class udp_sender(gr.basic_block):
    def __init__(self, host="127.0.0.1", port=5005, node_id=0):
        gr.basic_block.__init__(self,
            name="udp_sender",
            in_sig=None,   # No regular input signal, only messages
            out_sig=None)

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.node_id = node_id

        # Register message input port
        self.message_port_register_in(gr.pmt.intern("in"))
        self.set_msg_handler(gr.pmt.intern("in"), self.handle_msg)

    def handle_msg(self, msg):
        """Handles incoming messages and sends them over UDP."""
        try:
            msg = pmt.to_python(msg)
            mac_tx = [msg[0]['address 2'], msg[0]['address 1'], msg[0]['address 3']]
            if "e8:94:f6:09:ae:bd" in mac_tx:
                timestamp = timestamp = msg[0]['wifi_toa']
                # Split into integer (seconds) and fractional (nanoseconds)
                q, mod = divmod(timestamp, 1)
                seconds = int(q)
                nanoseconds = int((mod) * 1e9)

                try:
                    ssid = msg[0]['ssid']
                except KeyError:
                    ssid = "U"
                    
                # Create the dictionary message
                message = {
                    "node": self.node_id,
                    "wifi_toa_sec": seconds,  # Integer part (seconds)
                    "wifi_toa_nsec": nanoseconds,  # Fractional part (nanoseconds)
                    "mac": mac_tx,
                    "ssid": ssid,
                    "sequence number": msg[0]['sequence number'],
                    "snr": msg[0]['snr'],
                    "subtype": msg[0]['subtype'],
                    "type": msg[0]['type'],
                }
                
                # Send the serialized message over UDP
                print(f"Sending message: {message} to {self.host}:{self.port}")
                self.sock.sendto(str(message).encode('utf-8'), (self.host, self.port))
        except Exception as e:
            print(f"Error sending message: {e}")
