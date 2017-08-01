from Packet.ReceivedPacket import ReceivedPacket
from utils import *


class IGMP:
    def __init__(self):
        # Key: interface_name, Value: Interface_obj
        self.interfaces = {}

    def add_interface(self, interface):
        if interface.interface_name in self.interfaces:
            return

        self.interfaces[interface.interface_name] = interface

    # receive handler
    def receive_handle(self, packet: ReceivedPacket):
        interface = packet.interface
        ip_sender = packet.ip_header.ip_src
        print("ip = ", ip_sender)
        igmp_hdr = packet.igmp_header

        if igmp_hdr.type == Version_1_Membership_Report:
            interface.interface_state.receive_v1_membership_report(packet)
        elif igmp_hdr.type == Version_2_Membership_Report:
            interface.interface_state.receive_v2_membership_report(packet)

        elif igmp_hdr.type == Leave_Group:
            interface.interface_state.receive_leave_group(packet)

        elif igmp_hdr.type == Membership_Query:
            interface.interface_state.receive_query(packet)
        else:
            raise Exception
