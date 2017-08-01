import netifaces
from prettytable import PrettyTable
from Interface import Interface
import time

from State.Querier import Querier
from State.querier import CheckingMembership
from State.querier import MembersPresent
from State.querier import NoMembersPresent
from State.querier import Version1MembersPresent


interfaces = {}  # interfaces with igmp enabled
igmp = None

def add_interface(interface_name):
    global interfaces
    if interface_name not in interfaces:
        interface = Interface(interface_name)
        interfaces[interface_name] = interface


def remove_interface(interface_name):
    global interfaces
    global neighbors
    if (interface_name in interfaces) or interface_name == "*":
        if interface_name == "*":
            interface_name = list(interfaces.keys())
        else:
            interface_name = [interface_name]
        for if_name in interface_name:
            interfaces[if_name].remove()
            del interfaces[if_name]
        print("removido interface")

        for (ip_neighbor, neighbor) in list(neighbors.items()):
            if neighbor.contact_interface not in interfaces:
                neighbor.remove()


def list_enabled_interfaces():
    global interfaces
    t = PrettyTable(['Interface', 'IP', 'Enabled', 'State'])
    for interface in netifaces.interfaces():
        # TODO: fix same interface with multiple ips
        try:
            ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
        except Exception:
            continue
        enabled = interface in interfaces
        if enabled:
            state = interfaces[interface].interface_state.interface_state.name_state()
        else:
            state = "-"
        t.add_row([interface, ip, enabled, state])
    print(t)
    return str(t)

def list_state():
    check_time = time.time()
    t = PrettyTable(['Interface', 'RouterState', 'Group Adress', "Uptime", "GroupState"])
    for (interface_name, interface_obj) in list(interfaces.items()):
        interface_state = interface_obj.interface_state
        if interface_state.interface_state is Querier:
            state_txt = "Querier"
        else:
            state_txt = "Non Querier"

        print(state_txt)
        print(interface_state.group_state.items())

        for (group_addr, group_state) in list(interface_state.group_state.items()):
            print(group_addr)
            uptime = 0
            if group_state.state is CheckingMembership:
                group_state_txt = "CheckingMembership"
            elif group_state.state is MembersPresent:
                group_state_txt = "MembersPresent"
            elif group_state.state is NoMembersPresent:
                group_state_txt = "NoMembersPresent"
            elif group_state.state is Version1MembersPresent:
                group_state_txt = "Version1MembersPresent"
            else:
                print("upsupsups")
                continue
            t.add_row([interface_name, state_txt, group_addr, uptime, group_state_txt])
    return str(t)


def main(interfaces_to_add=[]):
    from IGMP import IGMP

    global igmp
    igmp = IGMP()

    for interface in interfaces_to_add:
        add_interface(interface)
