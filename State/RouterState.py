from Interface import Interface
from Packet.PacketIGMPHeader import PacketIGMPHeader
from Packet.ReceivedPacket import ReceivedPacket
from threading import Timer
from utils import *
from State.Querier import Querier


class RouterState:
    def __init__(self, interface: Interface):
        # interface of the router connected to the network
        self.interface = interface

        # state of the router (Querier/NonQuerier)
        self.interface_state = Querier

        # state of each group
        # Key: GroupAddress, Value: GroupState object
        self.group_state = {}

        # send general query
        packet = PacketIGMPHeader(type=Membership_Query, max_resp_time=MaxResponseTime)
        self.interface.send(packet.bytes())

        # set initial general query timer
        timer = Timer(QueryInterval, self.general_query_timeout)
        timer.start()
        self.general_query_timer = timer

        # present timer
        self.querier_present_timer = None


    ############################################
    # interface_state methods
    ############################################
    def general_query_timeout(self):
        self.interface_state.general_query_timeout(self)

    def querier_present_timeout(self):
        self.interface_state.querier_present_timeout(self)

    def receive_query(self, packet: ReceivedPacket):
        self.interface_state.receive_query(self, packet)


    ############################################
    # group state methods
    ############################################
    def receive_v1_membership_report(self, packet: ReceivedPacket):
        igmp_group = packet.igmp_header.group_address
        if igmp_group not in self.group_state:
            from State.GroupState import GroupState
            self.group_state[igmp_group] = GroupState(self, igmp_group)

        self.group_state[packet.igmp_header.group_address].receive_v1_membership_report(packet)

    def receive_v2_membership_report(self, packet: ReceivedPacket):
        igmp_group = packet.igmp_header.group_address
        if igmp_group not in self.group_state:
            from State.GroupState import GroupState
            self.group_state[igmp_group] = GroupState(self, igmp_group)

        self.group_state[packet.igmp_header.group_address].receive_v2_membership_report(packet)

    def receive_leave_group(self, packet: ReceivedPacket):
        igmp_group = packet.igmp_header.group_address
        if igmp_group not in self.group_state:
            from State.GroupState import GroupState
            self.group_state[igmp_group] = GroupState(self, igmp_group)

        self.group_state[packet.igmp_header.group_address].receive_leave_group(packet)
