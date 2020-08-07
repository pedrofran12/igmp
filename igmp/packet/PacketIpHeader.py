import struct
import socket


class PacketIpHeader:
    """
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |Version|
    +-+-+-+-+
    """
    IP_HDR = "! B"
    IP_HDR_LEN = struct.calcsize(IP_HDR)

    def __init__(self, ver, hdr_len):
        self.version = ver
        self.hdr_length = hdr_len

    def __len__(self):
        return self.hdr_length

    @staticmethod
    def parse_bytes(data: bytes):
        (verhlen, ) = struct.unpack(PacketIpHeader.IP_HDR, data[:PacketIpHeader.IP_HDR_LEN])
        ver = (verhlen & 0xF0) >> 4
        print("ver:", ver)
        return PACKET_HEADER.get(ver).parse_bytes(data)


class PacketIpv4Header(PacketIpHeader):
    """
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |Version|  IHL  |Type of Service|          Total Length         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |         Identification        |Flags|      Fragment Offset    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |  Time to Live |    Protocol   |         Header Checksum       |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                       Source Address                          |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Destination Address                        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Options                    |    Padding    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    IP_HDR = "! BBH HH BBH 4s 4s"
    IP_HDR_LEN = struct.calcsize(IP_HDR)

    def __init__(self, ver, hdr_len, ttl, proto, ip_src, ip_dst):
        super().__init__(ver, hdr_len)
        self.ttl = ttl
        self.proto = proto
        self.ip_src = ip_src
        self.ip_dst = ip_dst

    def __len__(self):
        return self.hdr_length

    @staticmethod
    def parse_bytes(data: bytes):
        (verhlen, tos, iplen, ipid, frag, ttl, proto, cksum, src, dst) = \
            struct.unpack(PacketIpv4Header.IP_HDR, data[:PacketIpv4Header.IP_HDR_LEN])

        ver = (verhlen & 0xf0) >> 4
        hlen = (verhlen & 0x0f) * 4

        '''
        "VER": ver,
        "HLEN": hlen,
        "TOS": tos,
        "IPLEN": iplen,
        "IPID": ipid,
        "FRAG": frag,
        "TTL": ttl,
        "PROTO": proto,
        "CKSUM": cksum,
        "SRC": socket.inet_ntoa(src),
        "DST": socket.inet_ntoa(dst)
        '''
        src_ip = socket.inet_ntoa(src)
        dst_ip = socket.inet_ntoa(dst)
        return PacketIpv4Header(ver, hlen, ttl, proto, src_ip, dst_ip)


PACKET_HEADER = {
    4: PacketIpv4Header,
}
