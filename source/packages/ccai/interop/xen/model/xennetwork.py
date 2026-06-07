"""
    .. module:: xennetwork
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI network object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenNetwork:
    """
        Typed record describing an XAPI network.

        :param uuid: The network uuid.
        :param name_label: The human-readable network label.
        :param name_description: The network description.
        :param bridge: The Linux bridge / OVS bridge backing the network.
        :param mtu: The configured network MTU.
    """
    uuid: str
    name_label: str
    name_description: str = ""
    bridge: str = ""
    mtu: int = 1500
