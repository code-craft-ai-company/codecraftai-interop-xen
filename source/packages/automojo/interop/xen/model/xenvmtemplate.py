"""
    .. module:: xenvmtemplate
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI VM template object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenVmTemplate:
    """
        Typed record describing an XAPI VM template.

        :param uuid: The template uuid.
        :param name_label: The human-readable template label.
        :param name_description: The template description.
        :param os_version_hint: A best-effort guest OS family/version hint.
    """
    uuid: str
    name_label: str
    name_description: str = ""
    os_version_hint: str = ""
