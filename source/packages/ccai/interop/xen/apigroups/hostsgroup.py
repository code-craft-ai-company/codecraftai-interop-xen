"""
    .. module:: hostsgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: HostsGroup — XAPI host enumeration.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import List

from ccai.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from ccai.interop.xen.apigroups.basegroup import BaseGroup
from ccai.interop.xen.model.xenhost import XenHost


class HostsGroup(BaseGroup):
    """
        XAPI ``host`` object-class operations.
    """

    def list(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
             ) -> List[XenHost]:
        """
            Enumerate the pool's hosts as :class:`XenHost` records.

            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenHost` records.
        """
        records = self._call(method_path="host.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenHost] = []
        if isinstance(records, dict):
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)
                out.append(XenHost(
                    uuid=record.get("uuid", ""),
                    name_label=record.get("name_label", ""),
                    address=record.get("address", ""),
                    enabled=bool(record.get("enabled", True)),
                ))
        rtnval = out
        return rtnval
