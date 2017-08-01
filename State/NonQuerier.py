from threading import Timer
from utils import *
from Packet.PacketIGMPHeader import PacketIGMPHeader
from Packet.ReceivedPacket import ReceivedPacket
from ipaddress import IPv4Address


class NonQuerier:

    @staticmethod
    def general_query_timeout(router_state):
        # do nothing
        return

    @staticmethod
    def querier_present_timeout(router_state):
        # send general query
        packet = PacketIGMPHeader(type=Membership_Query, max_resp_time=QueryResponseInterval)
        router_state.interface.send(packet.bytes())

        # set general query timer
        general_timer = router_state.general_query_timer
        if general_timer is not None:
            general_timer.cancel()
        general_query_timer = Timer(QueryInterval, router_state.general_query_timeout)
        general_query_timer.start()
        router_state.general_query_timer = general_query_timer

    @staticmethod
    def receive_query(router_state, packet: ReceivedPacket):
        source_ip = packet.ip_header.ip_src

        # if source ip of membership query not lower than the ip of the received interface => ignore
        if IPv4Address(source_ip) >= IPv4Address(router_state.interface.get_ip()):
            return

        # reset other present querier timer
        timer = router_state.querier_present_timer
        if timer is not None:
            timer.cancel()

        querier_present_timer = Timer(OtherQuerierPresentInterval, router_state.querier_present_timeout)
        querier_present_timer.start()
        router_state.querier_present_timer = querier_present_timer

    # TODO ver se existe uma melhor maneira de fazer isto
    @staticmethod
    def name_state():
        return "Non Querier"
