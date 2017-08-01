from Packet.PacketIGMPHeader import PacketIGMPHeader
from Packet.ReceivedPacket import ReceivedPacket
from State.querier import Version1MembersPresent, CheckingMembership
from State.querier import NoMembersPresent
from utils import *



def group_membership_timeout(router_state, group_addr: str):
    # TODO NOTIFY ROUTING - !!!!
    router_state.group_state[group_addr].state = NoMembersPresent


def group_membership_v1_timeout(router_state, group_addr: str):
    # do nothing
    return


def retransmit_timeout(router_state, group_addr: str):
    # do nothing
    return


def receive_v1_membership_report(router_state, packet: ReceivedPacket):
    group_ip = packet.igmp_header.group_address

    group_state = router_state.group_state[group_ip]
    group_state.set_timer()
    group_state.set_v1_host_timer()
    group_state.state = Version1MembersPresent


def receive_v2_membership_report(router_state, packet: ReceivedPacket):
    group_ip = packet.igmp_header.group_address

    group_state = router_state.group_state[group_ip]
    group_state.set_timer()

def receive_leave_group(router_state, packet: ReceivedPacket):
    group_ip = packet.igmp_header.group_address

    group_state = router_state.group_state[group_ip]
    group_state.set_timer(alternative=True)
    group_state.set_retransmit_timer()

    # todo dont send packet if router NonQuerier
    packet = PacketIGMPHeader(type=Membership_Query, max_resp_time=LastMemberQueryInterval, group_address=group_ip)
    router_state.interface.send(data=packet.bytes(), address=group_ip)

    group_state.state = CheckingMembership

