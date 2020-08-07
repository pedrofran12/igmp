# IGMP

This repository stores the implementation of IGMPv2 router-side state machines. This can be used to detect multicast interest of directly connected hosts.

The goal of this repository/module is to facilitate maintainability of this IGMP implementation since its code is used by other Python projects/modules:

- [HPIM-DM](https://github.com/pedrofran12/hpim_dm)
- [PIM-DM](https://github.com/pedrofran12/pim_dm)

This implementation was performed during my Master thesis and has since then been updated to fix issues, add new features and in the future to include the implementation of IGMPv3 as well.


# Documents detailing the initial work of IGMPv2 implementation

 - [Python implementation of IGMPv2, PIM-DM and HPIM-DM](https://github.com/pedrofran12/hpim_dm/tree/master/docs/PythonImplementations.pdf)
 - [Test to Python implementation of IGMPv2, PIM-DM, and HPIM-DM](https://github.com/pedrofran12/hpim_dm/tree/master/docs/PythonTests.pdf)


# Requirements

 - Linux machine
 - Python3 (we have written all code to be compatible with at least Python v3.2)
 - pip (to install all dependencies)


# Installation

  ```
  pip3 install igmp
  ```

# How to use it?

```python
# import module
from igmp import InterfaceIGMP

intf = InterfaceIGMP(interface_name="eth0") 

# get information from a given multicast group
multicast_group_obj = intf.interface_state.get_group_state(group_ip="224.10.11.12")

interest = multicast_group_obj.has_members()  # boolean that informs if there is multicast interest in this group
group_state = multicast_group_obj.state.print_state()  # get string identifying the state in which this group is at

# get notified of interest changes on this group
class MulticastGroupNotifier:
    def notify_membership(self, has_members):
        print(has_members)

notifier = MulticastGroupNotifier()
multicast_group_obj.add_multicast_routing_entry(notifier)

# when there is a change of multicast interest (for example group 224.10.11.12 gets interested receivers), the object associated to this object is notified through "notify_membership" method with has_members=True

# if you no longer want to monitor the interest of 224.10.11.12, remove the notifier from the group
multicast_group_obj.remove_multicast_routing_entry(notifier)
```
