"""
    .. module:: xenvifspec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Request spec for attaching an XAPI VIF.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenVifSpec:
    """
        Request spec for ``VIF.create``.

        :param vm_uuid: The uuid of the VM the VIF attaches to.
        :param network_uuid: The uuid of the network the VIF connects to.
        :param device: The guest-visible device slot.
        :param mac: The VIF MAC address (empty for auto-generation).
    """
    vm_uuid: str
    network_uuid: str
    device: str = "0"
    mac: str = ""
