"""
    .. module:: xenvif
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI VIF (virtual network interface).

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenVif:
    """
        Typed record describing an XAPI VIF.

        :param uuid: The VIF uuid.
        :param vm_uuid: The uuid of the VM the VIF belongs to.
        :param network_uuid: The uuid of the network the VIF attaches to.
        :param device: The guest-visible device slot (e.g. ``0``).
        :param mac: The VIF MAC address (empty for auto-generated).
    """
    uuid: str
    vm_uuid: str
    network_uuid: str
    device: str = "0"
    mac: str = ""
