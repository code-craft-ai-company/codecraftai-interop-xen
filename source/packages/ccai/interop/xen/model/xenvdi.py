"""
    .. module:: xenvdi
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI VDI (virtual disk image) object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenVdi:
    """
        Typed record describing an XAPI VDI.

        :param uuid: The VDI uuid.
        :param name_label: The human-readable VDI label.
        :param name_description: The VDI description.
        :param sr_uuid: The uuid of the SR hosting the VDI.
        :param virtual_size: The VDI size in bytes.
    """
    uuid: str
    name_label: str
    name_description: str = ""
    sr_uuid: str = ""
    virtual_size: int = 0
