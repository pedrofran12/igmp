import netifaces
from prettytable import PrettyTable
from Interface import Interface
import time



interfaces = {}  # interfaces with igmp enabled
igmp = None

def add_interface(interface_name):
    global interfaces
    if interface_name not in interfaces:
        interface = Interface(interface_name)
        interfaces[interface_name] = interface


def remove_interface(interface_name):
    global interfaces
    if (interface_name in interfaces) or interface_name == "*":
        if interface_name == "*":
            interface_name = list(interfaces.keys())
        else:
            interface_name = [interface_name]
        for if_name in interface_name:
            interfaces[if_name].remove()
            del interfaces[if_name]
        print("removido interface")

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
            state = interfaces[interface].interface_state.print_state()
        else:
            state = "-"
        t.add_row([interface, ip, enabled, state])
    print(t)
    return str(t)

def list_state():
    check_time = time.time()
    t = PrettyTable(['Interface', 'RouterState', 'Group Adress', 'Uptime', 'GroupState'])
    for (interface_name, interface_obj) in list(interfaces.items()):
        interface_state = interface_obj.interface_state
        state_txt = interface_state.print_state()
        print(interface_state.group_state.items())

        for (group_addr, group_state) in list(interface_state.group_state.items()):
            print(group_addr)
            uptime = 0
            group_state_txt = group_state.print_state()
            t.add_row([interface_name, state_txt, group_addr, uptime, group_state_txt])
    return str(t)


def main(interfaces_to_add=[]):
    from IGMP import IGMP

    global igmp
    igmp = IGMP()

    for interface in interfaces_to_add:
        add_interface(interface)
