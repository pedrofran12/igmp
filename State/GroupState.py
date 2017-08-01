from Packet.ReceivedPacket import ReceivedPacket
from State.Querier import Querier
from threading import Timer
from utils import *
from State.querier import NoMembersPresent


class GroupState:
    def __init__(self, router_state, group_ip, state=NoMembersPresent, timer=None, v1_host_timer = None, retransmit_timer=None):
        self.router_state = router_state
        self.group_ip = group_ip
        self.state = state
        self.timer = timer
        self.v1_host_timer = v1_host_timer
        self.retransmit_timer = retransmit_timer

    ###########################################
    # Set timers
    ###########################################
    def set_timer(self, alternative=False):
        if not alternative:
            time = GroupMembershipInterval
        else:
            if self.router_state is Querier:
                time = LastMemberQueryInterval * LastMemberQueryCount
            else:
                time = MaxResponseTime

        if self.timer is not None:
            self.timer.cancel()
        timer = Timer(time, self.group_membership_timeout)
        timer.start()
        self.timer = timer

    def set_v1_host_timer(self):
        if self.v1_host_timer is not None:
            self.v1_host_timer.cancel()
        v1_host_timer = Timer(GroupMembershipInterval, self.group_membership_v1_timeout)
        v1_host_timer.start()
        self.v1_host_timer = v1_host_timer

    def set_retransmit_timer(self):
        if self.retransmit_timer is not None:
            self.retransmit_timer.cancel()
        retransmit_timer = Timer(LastMemberQueryInterval, self.retransmit_timeout)
        retransmit_timer.start()
        self.retransmit_timer = retransmit_timer

    def clear_retransmit_timer(self):
        if self.retransmit_timer is not None:
            self.retransmit_timer.cancel()

    ###########################################
    # Timer timeout
    ###########################################
    def group_membership_timeout(self):
        self.state.group_membership_timeout(self.router_state, self.group_ip)

    def group_membership_v1_timeout(self):
        self.state.group_membership_v1_timeout(self.router_state, self.group_ip)

    def retransmit_timeout(self):
        self.state.retransmit_timeout(self.router_state, self.group_ip)

    ###########################################
    # Receive Packets
    ###########################################
    def receive_v1_membership_report(self, packet: ReceivedPacket):
        self.state.receive_v1_membership_report(self.router_state, packet)

    def receive_v2_membership_report(self, packet: ReceivedPacket):
        self.state.receive_v2_membership_report(self.router_state, packet)

    def receive_leave_group(self, packet: ReceivedPacket):
        self.state.receive_leave_group(self.router_state, packet)

