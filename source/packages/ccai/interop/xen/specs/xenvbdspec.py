"""
    .. module:: xenvbdspec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Request spec for attaching an XAPI VBD.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenVbdSpec:
    """
        Request spec for ``VBD.create``.

        :param vm_uuid: The uuid of the VM the VBD attaches to.
        :param vdi_uuid: The uuid of the VDI the VBD links to.
        :param userdevice: The guest-visible device slot.
        :param bootable: Whether the VBD is the boot device.
    """
    vm_uuid: str
    vdi_uuid: str
    userdevice: str = "0"
    bootable: bool = False
