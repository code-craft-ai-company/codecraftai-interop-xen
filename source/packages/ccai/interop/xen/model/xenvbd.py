"""
    .. module:: xenvbd
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI VBD (virtual block device) object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenVbd:
    """
        Typed record describing an XAPI VBD.

        :param uuid: The VBD uuid.
        :param vm_uuid: The uuid of the VM the VBD belongs to.
        :param vdi_uuid: The uuid of the VDI the VBD links to.
        :param userdevice: The guest-visible device slot (e.g. ``0``).
        :param bootable: Whether the VBD is the boot device.
    """
    uuid: str
    vm_uuid: str
    vdi_uuid: str
    userdevice: str = "0"
    bootable: bool = False
