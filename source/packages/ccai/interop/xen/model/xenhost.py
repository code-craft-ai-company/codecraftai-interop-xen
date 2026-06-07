"""
    .. module:: xenhost
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI host object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenHost:
    """
        Typed record describing an XAPI host.

        :param uuid: The host uuid.
        :param name_label: The human-readable host label.
        :param address: The host management IP address.
        :param enabled: Whether the host is enabled for VM placement.
    """
    uuid: str
    name_label: str
    address: str = ""
    enabled: bool = True
