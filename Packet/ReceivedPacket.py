from Packet.Packet import Packet
from Packet.PacketIpHeader import PacketIpHeader
from Packet.PacketIGMPHeader import PacketIGMPHeader

class ReceivedPacket(Packet):
    def __init__(self, raw_packet, interface):
        self.interface = interface
        # Parse ao packet e preencher objeto Packet

        packet_ip_hdr = raw_packet[:PacketIpHeader.IP_HDR_LEN]
        ip_header = PacketIpHeader.parse_bytes(packet_ip_hdr)

        packet_without_ip_hdr = raw_packet[ip_header.hdr_length:]
        igmp_header = PacketIGMPHeader.parse_bytes(packet_without_ip_hdr)

        super().__init__(ip_header=ip_header, igmp_header=igmp_header)
