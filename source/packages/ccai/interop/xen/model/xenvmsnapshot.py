"""
    .. module:: xenvmsnapshot
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI VM snapshot object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenVmSnapshot:
    """
        Typed record describing an XAPI VM snapshot.

        :param uuid: The snapshot VM uuid.
        :param name_label: The human-readable snapshot label.
        :param snapshot_of_uuid: The uuid of the VM the snapshot was taken of.
        :param snapshot_time: The XAPI snapshot timestamp string.
    """
    uuid: str
    name_label: str
    snapshot_of_uuid: str = ""
    snapshot_time: str = ""
