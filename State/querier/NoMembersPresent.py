from Packet.ReceivedPacket import ReceivedPacket
from State.querier import MembersPresent, Version1MembersPresent



def group_membership_timeout(router_state, group_addr: str):
    # do nothing
    return


def group_membership_v1_timeout(router_state, group_addr: str):
    # do nothing
    return


def retransmit_timeout(router_state, group_addr: str):
    # do nothing
    return


def receive_v1_membership_report(router_state, packet: ReceivedPacket):
    group_ip = packet.igmp_header.group_address
    # TODO NOTIFY ROUTING + !!!!

    group_state = router_state.group_state[group_ip]
    group_state.set_timer()
    group_state.set_v1_host_timer()
    group_state.state = Version1MembersPresent


def receive_v2_membership_report(router_state, packet: ReceivedPacket):
    group_ip = packet.igmp_header.group_address
    # TODO NOTIFY ROUTING + !!!!

    group_state = router_state.group_state[group_ip]
    group_state.set_timer()
    group_state.state = MembersPresent


def receive_leave_group(router_state, packet: ReceivedPacket):
    return

