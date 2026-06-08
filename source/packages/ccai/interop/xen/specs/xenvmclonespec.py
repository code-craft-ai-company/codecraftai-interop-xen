"""
    .. module:: xenvmclonespec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Request spec for cloning an XAPI VM from a template.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class XenVmCloneSpec:
    """
        Request spec for ``VM.clone`` followed by spec-override application.

        :param name_label: The new VM's name_label.
        :param name_description: The new VM's description.
        :param vcpus_max: Optional vCPU override applied after clone.
        :param memory_bytes: Optional static memory override (bytes).
        :param other_config: Key/value pairs merged into ``other_config``.
        :param tags: Tag strings applied to the cloned VM.
        :param xenstore_data: ``vm-data`` xenstore key/value pairs (cloud-init
                              user-data lives under ``vm-data/cloud-init``).
    """
    name_label: str
    name_description: str = ""
    vcpus_max: Optional[int] = None
    memory_bytes: Optional[int] = None
    other_config: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    xenstore_data: Dict[str, str] = field(default_factory=dict)
