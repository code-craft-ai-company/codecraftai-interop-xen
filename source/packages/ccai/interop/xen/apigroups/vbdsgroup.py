"""
    .. module:: vbdsgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: VbdsGroup — XAPI VBD attach/detach with idempotency.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import List, Optional

from ccai.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from ccai.interop.xen.apigroups.basegroup import BaseGroup
from ccai.interop.xen.exceptions.xenexceptions import XenError
from ccai.interop.xen.model.xenvbd import XenVbd
from ccai.interop.xen.specs.xenvbdspec import XenVbdSpec


class VbdsGroup(BaseGroup):
    """
        XAPI ``VBD`` object-class operations.
    """

    def list(self, *, vm_uuid: Optional[str] = None,
             aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> List[XenVbd]:
        """
            Enumerate VBDs as :class:`XenVbd` records.

            :param vm_uuid: Optional VM uuid filter.
            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenVbd` records.
        """
        records = self._call(method_path="VBD.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenVbd] = []
        if isinstance(records, dict):
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)
                vm_ref = record.get("VM", None)
                vdi_ref = record.get("VDI", None)
                resolved_vm = (self._resolver.maybe_uuid_for(opaque_ref=vm_ref)
                               if vm_ref is not None else None)
                resolved_vdi = (self._resolver.maybe_uuid_for(
                    opaque_ref=vdi_ref) if vdi_ref is not None else None)
                if vm_uuid is not None and resolved_vm != vm_uuid:
                    continue
                out.append(XenVbd(
                    uuid=record.get("uuid", ""),
                    vm_uuid=resolved_vm if resolved_vm is not None else "",
                    vdi_uuid=resolved_vdi if resolved_vdi is not None else "",
                    userdevice=record.get("userdevice", "0"),
                    bootable=bool(record.get("bootable", False)),
                ))
        rtnval = out
        return rtnval

    def attach(self, *, spec: XenVbdSpec,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> XenVbd:
        """
            Attach a VDI to a VM through a new VBD.

            Idempotent: when a VBD already links the same VM and VDI the
            existing record is returned.

            :param spec: The :class:`XenVbdSpec`.
            :param aspects: Behaviour controls.

            :returns: The created (or pre-existing) :class:`XenVbd`.
        """
        existing = self.list(vm_uuid=spec.vm_uuid, aspects=aspects)
        for vbd in existing:
            if vbd.vdi_uuid == spec.vdi_uuid:
                rtnval = vbd
                return rtnval

        vm_ref = self._resolver.ref_for(uuid=spec.vm_uuid)
        vdi_ref = self._resolver.ref_for(uuid=spec.vdi_uuid)
        vbd_record = {
            "VM": vm_ref,
            "VDI": vdi_ref,
            "userdevice": spec.userdevice,
            "bootable": spec.bootable,
            "mode": "RW",
            "type": "Disk",
            "empty": False,
            "other_config": {},
            "qos_algorithm_type": "",
            "qos_algorithm_params": {},
        }
        opaque_ref = self._call(method_path="VBD.create",
                                args=[vbd_record], aspects=aspects)
        uuid = self._call(method_path="VBD.get_uuid", args=[opaque_ref],
                          aspects=aspects)
        self._resolver.remember(opaque_ref=opaque_ref, uuid=uuid)

        rtnval = XenVbd(
            uuid=uuid, vm_uuid=spec.vm_uuid, vdi_uuid=spec.vdi_uuid,
            userdevice=spec.userdevice, bootable=spec.bootable,
        )
        return rtnval

    def detach(self, *, vbd_uuid: str,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Destroy a VBD by uuid.

            Idempotent: detaching an absent VBD succeeds as a no-op.

            :param vbd_uuid: The uuid of the VBD to destroy.
            :param aspects: Behaviour controls.
        """
        vbd_ref = self._resolver.maybe_ref_for(uuid=vbd_uuid)
        if vbd_ref is None:
            # An unknown uuid has no live VBD to destroy; this is a no-op.
            return
        try:
            self._call(method_path="VBD.destroy", args=[vbd_ref],
                       aspects=aspects)
        except XenError:
            pass
        self._resolver.forget_uuid(uuid=vbd_uuid)
        return
