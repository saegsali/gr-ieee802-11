import socket
from gnuradio import gr

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
        # template dict with dummy values
        msg_dict = {"node": "","wifi_toa": 0.0, "address 3": "", "address 2": "", "address 1": "", "sequence number": "", "ssid": "", "subtype": "", "type": "", "duration": "", "dlt": "", "frame bytes": "", "encoding": "", "snr": "", "nominal frequency": "", "frequency offset": "", "beta": "", "csi": []}
        msg_dict["node"] = self.node_id
        
        try:
            print("=+===========================================================")
            
            # Send the serialized message over UDP
            msg_str = str.split(str(msg), ") (")
            remove_chars = ["(", ")", "#", "[", "]", "'"]
            for c in remove_chars:
                msg_str = [m.replace(c, "") for m in msg_str]
                # print(f"Message: {msg_str}")
            for m in msg_str:
                tmp = m.split(" . ")
                # print(f"Tmp: {tmp}")
                if len(tmp) > 1:
                    try:
                        msg_dict[tmp[0]] = tmp[1]
                        print(f"Key: {tmp[0]}, Value: {tmp[1]}")
                    except:
                        print(f"Error parsing message: {tmp}")
                        pass

                
            self.sock.sendto(str(msg_dict).encode('utf-8'), (self.host, self.port))
        except Exception as e:
            print(f"Error sending UDP message: {e}")

if __name__ == "__main__":
    # Create the UDP sender block
    sender = udp_sender(host="127.0.0.1", port=5005)
    message = "((address 3 . 48:2c:d0:3c:db:82) (address 2 . 48:2c:d0:3c:db:82) (address 1 . ff:ff:ff:ff:ff:ff) (sequence number . 212) (ssid . eduroam) (subtype . Beacon) (type . management) (duration . 0) (dlt . 105) (frame bytes . 370) (encoding . 0) (snr . 18.5551) (nominal frequency . 2.412e+09) (frequency offset . -21147.7) (beta . 0.907213) (csi . #[(0.566118,-0.298401) (0.631518,-0.245726) (0.657571,-0.144538) (0.690639,0.0103949) (0.678849,0.072456) (0.680707,0.0461684) (0.591707,0.162084) (0.478976,0.212965) (0.451279,0.239542) (0.387056,0.253145) (0.250386,0.159893) (0.191558,0.107284) (0.171853,0.118913) (0.0702613,-0.0185443) (0.109905,-0.146988) (0.0742382,-0.270683) (0.165585,-0.379584) (0.168831,-0.497667) (0.354727,-0.591889) (0.437455,-0.557083) (0.570716,-0.612538) (0.77234,-0.635723) (0.912641,-0.598075) (0.93393,-0.483502) (1.00211,-0.349984) (1.08942,-0.176415) (0.943632,0.156554) (0.82913,0.334521) (0.568084,0.285006) (0.462272,0.267365) (0.253101,0.193681) (0.109876,0.0587345) (0.087862,-0.102265) (0.031854,-0.287846) (0.198047,-0.43826) (0.38686,-0.529481) (0.521877,-0.604409) (0.747475,-0.603303) (0.99424,-0.58217) (1.12874,-0.440593) (1.28294,-0.222313) (1.36439,0.0103244) (1.27361,0.252473) (1.2032,0.410093) (1.0735,0.546541) (0.885395,0.565614) (0.754109,0.613179) (0.580458,0.516457) (0.556105,0.360515) (0.411728,0.209677) (0.452793,0.0442217) (0.580392,-0.111653)]) (wifi_toa . 0.297104))"
    sender.handle_msg(message)