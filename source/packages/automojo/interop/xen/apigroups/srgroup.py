"""
    .. module:: srgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: SrGroup — XAPI storage repository enumeration.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from typing import List

from automojo.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from automojo.interop.xen.apigroups.basegroup import BaseGroup
from automojo.interop.xen.model.xenstoragerepository import (
    XenStorageRepository
)


class SrGroup(BaseGroup):
    """
        XAPI ``SR`` object-class operations.
    """

    def list(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
             ) -> List[XenStorageRepository]:
        """
            Enumerate storage repositories as :class:`XenStorageRepository`
            records.

            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenStorageRepository` records.
        """
        records = self._call(method_path="SR.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenStorageRepository] = []
        if isinstance(records, dict):
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)
                out.append(XenStorageRepository(
                    uuid=record.get("uuid", ""),
                    name_label=record.get("name_label", ""),
                    type=record.get("type", ""),
                    physical_size=int(record.get("physical_size", 0)),
                    physical_utilisation=int(
                        record.get("physical_utilisation", 0)),
                    shared=bool(record.get("shared", False)),
                ))
        rtnval = out
        return rtnval
