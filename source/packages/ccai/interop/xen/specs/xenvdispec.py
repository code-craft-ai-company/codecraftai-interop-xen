"""
    .. module:: xenvdispec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Request spec for creating an XAPI VDI.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenVdiSpec:
    """
        Request spec for ``VDI.create``.

        :param name_label: The human-readable VDI label.
        :param sr_uuid: The uuid of the SR the VDI is created on.
        :param virtual_size: The VDI size in bytes.
        :param name_description: The VDI description.
    """
    name_label: str
    sr_uuid: str
    virtual_size: int
    name_description: str = ""
