from Packet.PacketIpHeader import PacketIpHeader
from Packet.PacketIGMPHeader import PacketIGMPHeader


class Packet:
    def __init__(self, ip_header: PacketIpHeader = None, igmp_header: PacketIGMPHeader = None):
        self.ip_header = ip_header
        self.igmp_header = igmp_header

    def bytes(self):
        return self.igmp_header.bytes()
