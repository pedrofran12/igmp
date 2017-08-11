import array


def checksum(pkt: bytes) -> bytes:
    if len(pkt) % 2 == 1:
        pkt += "\0"
    s = sum(array.array("H", pkt))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    s = ~s
    return (((s >> 8) & 0xff) | s << 8) & 0xffff

# obtain TYPE_CHECKING (for type hinting)
try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

# IGMP timers (in seconds)
RobustnessVariable = 2
QueryInterval = 125
QueryResponseInterval = 10
MaxResponseTime_QueryResponseInterval = QueryResponseInterval*10
GroupMembershipInterval = RobustnessVariable * QueryInterval + QueryResponseInterval
OtherQuerierPresentInterval = RobustnessVariable * QueryInterval + QueryResponseInterval/2
StartupQueryInterval = QueryInterval / 4
StartupQueryCount = RobustnessVariable
LastMemberQueryInterval = 1
MaxResponseTime_LastMemberQueryInterval = LastMemberQueryInterval*10
LastMemberQueryCount = RobustnessVariable
UnsolicitedReportInterval = 10
Version1RouterPresentTimeout = 400

# IGMP msg type
Membership_Query = 0x11
Version_1_Membership_Report = 0x12
Version_2_Membership_Report = 0x16
Leave_Group = 0x17
