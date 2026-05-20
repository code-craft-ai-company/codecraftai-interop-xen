"""
    .. module:: xenvm
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI VM object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class XenVm:
    """
        Typed record describing an XAPI VM.

        :param uuid: The VM uuid.
        :param name_label: The human-readable VM label.
        :param name_description: The VM description.
        :param power_state: The VM power state (Halted, Running, ...).
        :param vcpus_max: The maximum number of virtual CPUs.
        :param memory_static_max: The static maximum memory in bytes.
        :param is_a_template: Whether the VM is in fact a template.
        :param is_control_domain: Whether the VM is the host control domain.
        :param other_config: The XAPI ``other_config`` key/value map.
        :param tags: The XAPI ``tags`` string list.
    """
    uuid: str
    name_label: str
    name_description: str = ""
    power_state: str = "Halted"
    vcpus_max: int = 1
    memory_static_max: int = 0
    is_a_template: bool = False
    is_control_domain: bool = False
    other_config: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
