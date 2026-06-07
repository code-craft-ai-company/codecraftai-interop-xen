"""
    .. module:: xenpool
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI Pool object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass
from typing import Optional


@dataclass
class XenPool:
    """
        Typed record describing an XAPI Pool.

        :param uuid: The pool uuid.
        :param name_label: The human-readable pool label.
        :param name_description: The pool description.
        :param master_uuid: The uuid of the host acting as pool master.
    """
    uuid: str
    name_label: str
    name_description: str = ""
    master_uuid: Optional[str] = None
