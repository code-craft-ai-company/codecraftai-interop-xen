"""
    .. module:: snapshotsgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: SnapshotsGroup — XAPI VM snapshot create/list/revert/destroy.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import List

from ccai.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from ccai.interop.xen.apigroups.basegroup import BaseGroup
from ccai.interop.xen.exceptions.xenexceptions import is_handle_invalid, XenError
from ccai.interop.xen.model.xenvmsnapshot import XenVmSnapshot


class SnapshotsGroup(BaseGroup):
    """
        XAPI VM-snapshot operations.
    """

    def snapshot_vm(self, *, vm_uuid: str, name: str,
                    aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                    ) -> XenVmSnapshot:
        """
            Take a snapshot of a VM.

            :param vm_uuid: The uuid of the VM to snapshot.
            :param name: The snapshot name_label.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenVmSnapshot` record.
        """
        vm_ref = self._resolver.ref_for(uuid=vm_uuid)
        snap_ref = self._call(method_path="VM.snapshot",
                              args=[vm_ref, name], aspects=aspects)
        record = self._call(method_path="VM.get_record", args=[snap_ref],
                            aspects=aspects)
        self._record_ref(opaque_ref=snap_ref, record=record)

        snapshot_of = ""
        if isinstance(record, dict):
            of_ref = record.get("snapshot_of", None)
            if of_ref is not None:
                resolved = self._resolver.maybe_uuid_for(opaque_ref=of_ref)
                if resolved is not None:
                    snapshot_of = resolved

        rtnval = XenVmSnapshot(
            uuid=record.get("uuid", "") if isinstance(record, dict) else "",
            name_label=name, snapshot_of_uuid=snapshot_of,
            snapshot_time=record.get("snapshot_time", "")
            if isinstance(record, dict) else "",
        )
        return rtnval

    def list(self, *, vm_uuid: str,
             aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
             ) -> List[XenVmSnapshot]:
        """
            Enumerate the snapshots of a VM.

            :param vm_uuid: The uuid of the VM whose snapshots to list.
            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenVmSnapshot` records.
        """
        records = self._call(method_path="VM.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenVmSnapshot] = []
        if isinstance(records, dict):
            # Pre-pass: record every ref first so a snapshot's snapshot_of ->
            # parent-uuid resolution does not depend on dict iteration order. The
            # prior single-pass dropped snapshots whose record preceded their
            # parent VM record.
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)

            for opaque_ref, record in records.items():
                if bool(record.get("is_a_snapshot", False)) is not True:
                    continue
                of_ref = record.get("snapshot_of", None)
                resolved = (self._resolver.maybe_uuid_for(opaque_ref=of_ref)
                            if of_ref is not None else None)
                if resolved != vm_uuid:
                    continue
                out.append(XenVmSnapshot(
                    uuid=record.get("uuid", ""),
                    name_label=record.get("name_label", ""),
                    snapshot_of_uuid=resolved if resolved is not None
                    else "",
                    snapshot_time=record.get("snapshot_time", ""),
                ))
        rtnval = out
        return rtnval

    def revert(self, *, snapshot_uuid: str,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Revert a VM to one of its snapshots.

            :param snapshot_uuid: The uuid of the snapshot to revert to.
            :param aspects: Behaviour controls.
        """
        snap_ref = self._resolver.ref_for(uuid=snapshot_uuid)
        self._call(method_path="VM.revert", args=[snap_ref], aspects=aspects)
        return

    def destroy(self, *, snapshot_uuid: str,
                aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Destroy a VM snapshot by uuid.

            Idempotent: destroying an absent snapshot succeeds as a no-op.

            :param snapshot_uuid: The uuid of the snapshot to destroy.
            :param aspects: Behaviour controls.
        """
        snap_ref = self._resolver.maybe_ref_for(uuid=snapshot_uuid)
        if snap_ref is None:
            # An unknown uuid has no live snapshot to destroy; a no-op.
            return
        try:
            self._call(method_path="VM.destroy", args=[snap_ref],
                       aspects=aspects)
        except XenError as xerr:
            if not is_handle_invalid(xerr):
                raise
        self._resolver.forget_uuid(uuid=snapshot_uuid)
        return
