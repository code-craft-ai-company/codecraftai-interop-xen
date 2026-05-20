"""
    .. module:: poolgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: PoolGroup — XAPI pool enumeration.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import os

from automojo.errors.exceptions import SemanticError

from automojo.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from automojo.interop.xen.apigroups.basegroup import BaseGroup
from automojo.interop.xen.model.xenpool import XenPool


class PoolGroup(BaseGroup):
    """
        XAPI ``pool`` object-class operations.
    """

    def get(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> XenPool:
        """
            Return the single :class:`XenPool` record for the pool.

            :param aspects: Behaviour controls.

            :returns: A :class:`XenPool` record.
            :raises: SemanticError
        """
        records = self._call(method_path="pool.get_all_records", args=[],
                              aspects=aspects)
        if not isinstance(records, dict) or len(records) == 0:
            err_msg_lines = ["XAPI pool.get_all_records returned no pool."]
            err_msg = os.linesep.join(err_msg_lines)
            raise SemanticError(err_msg)

        opaque_ref, record = next(iter(records.items()))
        self._record_ref(opaque_ref=opaque_ref, record=record)

        master_ref = record.get("master", None)
        master_uuid = None
        if master_ref is not None:
            master_uuid = self._resolver.maybe_uuid_for(opaque_ref=master_ref)

        rtnval = XenPool(
            uuid=record.get("uuid", ""),
            name_label=record.get("name_label", ""),
            name_description=record.get("name_description", ""),
            master_uuid=master_uuid,
        )
        return rtnval
