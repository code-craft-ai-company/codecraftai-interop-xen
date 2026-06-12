"""
    .. module:: vdigroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: VdiGroup — XAPI VDI create/list/delete/resize.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import List, Optional

from ccai.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from ccai.interop.xen.apigroups.basegroup import BaseGroup
from ccai.interop.xen.exceptions.xenexceptions import is_handle_invalid, XenError
from ccai.interop.xen.model.xenvdi import XenVdi
from ccai.interop.xen.specs.xenvdispec import XenVdiSpec


class VdiGroup(BaseGroup):
    """
        XAPI ``VDI`` object-class operations.
    """

    def list(self, *, sr_uuid: Optional[str] = None,
             aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> List[XenVdi]:
        """
            Enumerate VDIs as :class:`XenVdi` records.

            :param sr_uuid: Optional SR uuid filter.
            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenVdi` records.
        """
        records = self._call(method_path="VDI.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenVdi] = []
        if isinstance(records, dict):
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)
                sr_ref = record.get("SR", None)
                resolved_sr = None
                if sr_ref is not None:
                    resolved_sr = self._resolver.maybe_uuid_for(
                        opaque_ref=sr_ref)
                if sr_uuid is not None and resolved_sr != sr_uuid:
                    continue
                out.append(XenVdi(
                    uuid=record.get("uuid", ""),
                    name_label=record.get("name_label", ""),
                    name_description=record.get("name_description", ""),
                    sr_uuid=resolved_sr if resolved_sr is not None else "",
                    virtual_size=int(record.get("virtual_size", 0)),
                ))
        rtnval = out
        return rtnval

    def create(self, *, spec: XenVdiSpec,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> XenVdi:
        """
            Create a VDI from a :class:`XenVdiSpec`.

            When a VDI with the same ``name_label`` already exists on the
            target SR the existing record is returned (read-before-create).

            :param spec: The VDI request spec.
            :param aspects: Behaviour controls.

            :returns: The created (or pre-existing) :class:`XenVdi` record.
        """
        existing = self.list(sr_uuid=spec.sr_uuid, aspects=aspects)
        for vdi in existing:
            if vdi.name_label == spec.name_label:
                rtnval = vdi
                return rtnval

        sr_ref = self._resolver.ref_for(uuid=spec.sr_uuid)
        vdi_record = {
            "name_label": spec.name_label,
            "name_description": spec.name_description,
            "SR": sr_ref,
            "virtual_size": str(spec.virtual_size),
            "type": "user",
            "sharable": False,
            "read_only": False,
            "other_config": {},
        }
        opaque_ref = self._call(method_path="VDI.create",
                                args=[vdi_record], aspects=aspects)
        uuid = self._call(method_path="VDI.get_uuid", args=[opaque_ref],
                          aspects=aspects)
        self._resolver.remember(opaque_ref=opaque_ref, uuid=uuid)

        rtnval = XenVdi(
            uuid=uuid, name_label=spec.name_label,
            name_description=spec.name_description, sr_uuid=spec.sr_uuid,
            virtual_size=spec.virtual_size,
        )
        return rtnval

    def delete(self, *, vdi_uuid: str,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Destroy a VDI by uuid.

            Idempotent: deleting an unknown VDI succeeds as a no-op.

            :param vdi_uuid: The uuid of the VDI to destroy.
            :param aspects: Behaviour controls.
        """
        vdi_ref = self._resolver.maybe_ref_for(uuid=vdi_uuid)
        if vdi_ref is None:
            # An unknown uuid has no live VDI to destroy; this is a no-op.
            return

        try:
            self._call(method_path="VDI.destroy", args=[vdi_ref],
                       aspects=aspects)
        except XenError as xerr:
            # Only an already-absent handle makes delete a no-op; other XAPI faults
            # are genuine failures and must surface.
            if not is_handle_invalid(xerr):
                raise
        self._resolver.forget_uuid(uuid=vdi_uuid)
        return

    def resize(self, *, vdi_uuid: str, size_bytes: int,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Resize a VDI to a new size in bytes.

            :param vdi_uuid: The uuid of the VDI to resize.
            :param size_bytes: The new VDI size in bytes.
            :param aspects: Behaviour controls.
        """
        vdi_ref = self._resolver.ref_for(uuid=vdi_uuid)
        self._call(method_path="VDI.resize",
                   args=[vdi_ref, str(size_bytes)], aspects=aspects)
        return
