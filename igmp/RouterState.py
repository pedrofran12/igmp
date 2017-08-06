from Interface import Interface
from Packet.PacketIGMPHeader import PacketIGMPHeader
from Packet.ReceivedPacket import ReceivedPacket
from threading import Timer
from utils import Membership_Query, QueryResponseInterval, QueryInterval, OtherQuerierPresentInterval
from .querier.Querier import Querier
from .nonquerier.NonQuerier import NonQuerier


class RouterState(object):
    def __init__(self, interface: Interface):
        # interface of the router connected to the network
        self.interface = interface

        # state of the router (Querier/NonQuerier)
        self.interface_state = Querier

        # state of each group
        # Key: GroupIPAddress, Value: GroupState object
        self.group_state = {}

        # send general query
        packet = PacketIGMPHeader(type=Membership_Query, max_resp_time=QueryResponseInterval)
        self.interface.send(packet.bytes())

        # set initial general query timer
        timer = Timer(QueryInterval, self.general_query_timeout)
        timer.start()
        self.general_query_timer = timer

        # present timer
        self.querier_present_timer = None

    # Send packet via interface
    def send(self, data, address):
        self.interface.send(data, address)

    ############################################
    # interface_state methods
    ############################################
    def print_state(self):
        return self.interface_state.state_name()

    def set_general_query_timer(self):
        self.clear_general_query_timer()
        general_query_timer = Timer(QueryInterval, self.general_query_timeout)
        general_query_timer.start()
        self.general_query_timer = general_query_timer

    def clear_general_query_timer(self):
        if self.general_query_timer is not None:
            self.general_query_timer.cancel()

    def set_querier_present_timer(self):
        self.clear_querier_present_timer()
        querier_present_timer = Timer(OtherQuerierPresentInterval, self.querier_present_timeout)
        querier_present_timer.start()
        self.querier_present_timer = querier_present_timer

    def clear_querier_present_timer(self):
        if self.querier_present_timer is not None:
            self.querier_present_timer.cancel()

    def general_query_timeout(self):
        self.interface_state.general_query_timeout(self)

    def querier_present_timeout(self):
        self.interface_state.querier_present_timeout(self)

    def change_interface_state(self, querier: bool):
        if querier:
            self.interface_state = Querier
        else:
            self.interface_state = NonQuerier

    ############################################
    # group state methods
    ############################################
    def receive_v1_membership_report(self, packet: ReceivedPacket):
        igmp_group = packet.igmp_header.group_address
        if igmp_group not in self.group_state:
            from .GroupState import GroupState
            self.group_state[igmp_group] = GroupState(self, igmp_group)

        self.group_state[igmp_group].receive_v1_membership_report()

    def receive_v2_membership_report(self, packet: ReceivedPacket):
        igmp_group = packet.igmp_header.group_address
        if igmp_group not in self.group_state:
            from .GroupState import GroupState
            self.group_state[igmp_group] = GroupState(self, igmp_group)

        self.group_state[igmp_group].receive_v2_membership_report()

    def receive_leave_group(self, packet: ReceivedPacket):
        igmp_group = packet.igmp_header.group_address
        if igmp_group in self.group_state:
            self.group_state[igmp_group].receive_leave_group()

    def receive_query(self, packet: ReceivedPacket):
        self.interface_state.receive_query(self, packet)
        igmp_group = packet.igmp_header.group_address

        # process group specific query
        if igmp_group != "0.0.0.0" and igmp_group in self.group_state:
            max_response_time = packet.igmp_header.max_resp_time
            self.group_state[igmp_group].receive_group_specific_query(max_response_time)
