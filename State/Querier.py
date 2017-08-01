from Packet.PacketIGMPHeader import PacketIGMPHeader
from Packet.ReceivedPacket import ReceivedPacket
from State.NonQuerier import NonQuerier
from threading import Timer
from utils import *
from ipaddress import IPv4Address


class Querier:

    @staticmethod
    def general_query_timeout(router_state):
        # send general query
        packet = PacketIGMPHeader(type=Membership_Query, max_resp_time=QueryResponseInterval)
        router_state.interface.send(packet.bytes())

        # set general query timer
        timer = Timer(QueryInterval, router_state.general_query_timeout)
        timer.start()
        router_state.general_query_timer = timer

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
        router_state.interface_state = NonQuerier

        # set other present querier timer
        timer = router_state.general_query_timer
        if timer is not None:
            timer.cancel()
            router_state.general_query_timer = None

        timer = router_state.querier_present_timer
        if timer is not None:
            timer.cancel()
        querier_present_timer = Timer(OtherQuerierPresentInterval, router_state.querier_present_timeout)
        querier_present_timer.start()
        router_state.querier_present_timer = querier_present_timer

    # TODO ver se existe uma melhor maneira de fazer isto
    @staticmethod
    def name_state():
        return "Querier"
