from Packet.PacketIGMPHeader import PacketIGMPHeader
from Packet.ReceivedPacket import ReceivedPacket
from utils import Membership_Query, QueryResponseInterval, LastMemberQueryCount, LastMemberQueryInterval
from ipaddress import IPv4Address


class Querier:
    @staticmethod
    def general_query_timeout(router_state):
        # send general query
        packet = PacketIGMPHeader(type=Membership_Query, max_resp_time=QueryResponseInterval)
        router_state.interface.send(packet.bytes())

        # set general query timer
        router_state.set_general_query_timer()

    @staticmethod
    def querier_present_timeout(router_state):
        # do nothing
        return

    @staticmethod
    def receive_query(router_state, packet: ReceivedPacket):
        source_ip = packet.ip_header.ip_src

        # if source ip of membership query not lower than the ip of the received interface => ignore
        if IPv4Address(source_ip) >= IPv4Address(router_state.interface.get_ip()):
            return

        # if source ip of membership query lower than the ip of the received interface => change state
        # change state of interface
        # Querier -> Non Querier
        router_state.change_interface_state(querier=False)

        # set other present querier timer
        router_state.clear_general_query_timer()
        router_state.set_querier_present_timer()


    # TODO ver se existe uma melhor maneira de fazer isto
    @staticmethod
    def state_name():
        return "Querier"

    @staticmethod
    def get_group_membership_time(max_response_time: int):
        return LastMemberQueryInterval * LastMemberQueryCount


    # State
    @staticmethod
    def get_checking_membership_state():
        from . import CheckingMembership
        return CheckingMembership

    @staticmethod
    def get_members_present_state():
        from . import MembersPresent
        return MembersPresent

    @staticmethod
    def get_no_members_present_state():
        from . import NoMembersPresent
        return NoMembersPresent

    @staticmethod
    def get_version_1_members_present_state():
        from . import Version1MembersPresent
        return Version1MembersPresent
