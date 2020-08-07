from .Packet import Packet
from .PacketIpHeader import PacketIpv4Header
from .PacketIGMPHeader import PacketIGMPHeader
from igmp.utils import TYPE_CHECKING
if TYPE_CHECKING:
    from igmp.Interface import Interface


class ReceivedPacket(Packet):
    # choose payload protocol class based on ip protocol number
    payload_protocol = {2: PacketIGMPHeader}

    def __init__(self, raw_packet: bytes, interface: 'Interface'):
        self.interface = interface

        # Parse packet and fill Packet super class
        ip_header = PacketIpv4Header.parse_bytes(raw_packet)
        protocol_number = ip_header.proto

        packet_without_ip_hdr = raw_packet[ip_header.hdr_length:]
        payload = ReceivedPacket.payload_protocol[protocol_number].parse_bytes(packet_without_ip_hdr)

        super().__init__(ip_header=ip_header, payload=payload)
