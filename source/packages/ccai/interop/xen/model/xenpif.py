"""
    .. module:: xenpif
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI PIF (physical interface) object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenPif:
    """
        Typed record describing an XAPI PIF.

        :param uuid: The PIF uuid.
        :param device: The interface device name (e.g. ``eth0``).
        :param host_uuid: The uuid of the host the PIF belongs to.
        :param network_uuid: The uuid of the network the PIF is attached to.
        :param management: Whether the PIF carries management traffic.
    """
    uuid: str
    device: str
    host_uuid: str
    network_uuid: str
    management: bool = False
