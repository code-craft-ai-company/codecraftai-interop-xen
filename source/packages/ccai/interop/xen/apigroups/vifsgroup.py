"""
    .. module:: vifsgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: VifsGroup — XAPI VIF attach/detach with idempotency.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import List, Optional

from ccai.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from ccai.interop.xen.apigroups.basegroup import BaseGroup
from ccai.interop.xen.exceptions.xenexceptions import XenError
from ccai.interop.xen.model.xenvif import XenVif
from ccai.interop.xen.specs.xenvifspec import XenVifSpec


class VifsGroup(BaseGroup):
    """
        XAPI ``VIF`` object-class operations.
    """

    def list(self, *, vm_uuid: Optional[str] = None,
             aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> List[XenVif]:
        """
            Enumerate VIFs as :class:`XenVif` records.

            :param vm_uuid: Optional VM uuid filter.
            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenVif` records.
        """
        records = self._call(method_path="VIF.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenVif] = []
        if isinstance(records, dict):
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)
                vm_ref = record.get("VM", None)
                net_ref = record.get("network", None)
                resolved_vm = (self._resolver.maybe_uuid_for(opaque_ref=vm_ref)
                               if vm_ref is not None else None)
                resolved_net = (self._resolver.maybe_uuid_for(
                    opaque_ref=net_ref) if net_ref is not None else None)
                if vm_uuid is not None and resolved_vm != vm_uuid:
                    continue
                out.append(XenVif(
                    uuid=record.get("uuid", ""),
                    vm_uuid=resolved_vm if resolved_vm is not None else "",
                    network_uuid=resolved_net if resolved_net is not None
                    else "",
                    device=record.get("device", "0"),
                    mac=record.get("MAC", record.get("mac", "")),
                ))
        rtnval = out
        return rtnval

    def attach(self, *, spec: XenVifSpec,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> XenVif:
        """
            Attach a VM to a network through a new VIF.

            Idempotent: when a VIF on the same device already links the VM
            and network the existing record is returned.

            :param spec: The :class:`XenVifSpec`.
            :param aspects: Behaviour controls.

            :returns: The created (or pre-existing) :class:`XenVif`.
        """
        existing = self.list(vm_uuid=spec.vm_uuid, aspects=aspects)
        for vif in existing:
            if (vif.network_uuid == spec.network_uuid
                    and vif.device == spec.device):
                rtnval = vif
                return rtnval

        vm_ref = self._resolver.ref_for(uuid=spec.vm_uuid)
        net_ref = self._resolver.ref_for(uuid=spec.network_uuid)
        vif_record = {
            "VM": vm_ref,
            "network": net_ref,
            "device": spec.device,
            "MAC": spec.mac,
            "MTU": "1500",
            "other_config": {},
            "qos_algorithm_type": "",
            "qos_algorithm_params": {},
        }
        opaque_ref = self._call(method_path="VIF.create",
                                args=[vif_record], aspects=aspects)
        uuid = self._call(method_path="VIF.get_uuid", args=[opaque_ref],
                          aspects=aspects)
        self._resolver.remember(opaque_ref=opaque_ref, uuid=uuid)

        rtnval = XenVif(
            uuid=uuid, vm_uuid=spec.vm_uuid,
            network_uuid=spec.network_uuid, device=spec.device,
            mac=spec.mac,
        )
        return rtnval

    def detach(self, *, vif_uuid: str,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Destroy a VIF by uuid.

            Idempotent: detaching an absent VIF succeeds as a no-op.

            :param vif_uuid: The uuid of the VIF to destroy.
            :param aspects: Behaviour controls.
        """
        vif_ref = self._resolver.maybe_ref_for(uuid=vif_uuid)
        if vif_ref is None:
            # An unknown uuid has no live VIF to destroy; this is a no-op.
            return
        try:
            self._call(method_path="VIF.destroy", args=[vif_ref],
                       aspects=aspects)
        except XenError:
            pass
        self._resolver.forget_uuid(uuid=vif_uuid)
        return
