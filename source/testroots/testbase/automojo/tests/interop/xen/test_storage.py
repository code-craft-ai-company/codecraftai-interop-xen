"""
    .. module:: test_storage
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: VDI create/list/delete/resize tests for the Vdi api-group.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from ccai.interop.xen.model.xenvdi import XenVdi
from ccai.interop.xen.specs.xenvdispec import XenVdiSpec


def _seed_sr_ref(client, fast_aspects) -> None:
    """
        Enumerate SRs so the resolver knows the SR opaque-ref/uuid pair.
    """
    client.Sr.list(aspects=fast_aspects)
    return


def test_vdi_create_returns_typed_record(client, fast_aspects) -> None:
    """
        Vdi.create creates a VDI and returns a typed XenVdi record.
    """
    _seed_sr_ref(client, fast_aspects)
    spec = XenVdiSpec(name_label="data-disk", sr_uuid="sr-uuid-1",
                      virtual_size=10737418240)
    vdi = client.Vdi.create(spec=spec, aspects=fast_aspects)
    assert isinstance(vdi, XenVdi)
    assert vdi.name_label == "data-disk"
    assert vdi.sr_uuid == "sr-uuid-1"
    assert vdi.virtual_size == 10737418240
    return


def test_vdi_create_is_idempotent_by_name_label(client,
                                                fast_aspects) -> None:
    """
        Creating a VDI with an existing name_label returns the existing one.
    """
    _seed_sr_ref(client, fast_aspects)
    spec = XenVdiSpec(name_label="data-disk", sr_uuid="sr-uuid-1",
                      virtual_size=10737418240)
    first = client.Vdi.create(spec=spec, aspects=fast_aspects)
    second = client.Vdi.create(spec=spec, aspects=fast_aspects)
    assert first.uuid == second.uuid
    assert len(client.Vdi.list(aspects=fast_aspects)) == 1
    return


def test_vdi_list_filters_by_sr(client, fast_aspects) -> None:
    """
        Vdi.list filters records by sr_uuid when one is supplied.
    """
    _seed_sr_ref(client, fast_aspects)
    spec = XenVdiSpec(name_label="d1", sr_uuid="sr-uuid-1",
                      virtual_size=1024)
    client.Vdi.create(spec=spec, aspects=fast_aspects)

    on_sr = client.Vdi.list(sr_uuid="sr-uuid-1", aspects=fast_aspects)
    assert len(on_sr) == 1

    off_sr = client.Vdi.list(sr_uuid="sr-other", aspects=fast_aspects)
    assert len(off_sr) == 0
    return


def test_vdi_delete_removes_record(client, fast_aspects) -> None:
    """
        Vdi.delete destroys a VDI by uuid.
    """
    _seed_sr_ref(client, fast_aspects)
    spec = XenVdiSpec(name_label="d1", sr_uuid="sr-uuid-1",
                      virtual_size=1024)
    vdi = client.Vdi.create(spec=spec, aspects=fast_aspects)
    client.Vdi.delete(vdi_uuid=vdi.uuid, aspects=fast_aspects)
    assert len(client.Vdi.list(aspects=fast_aspects)) == 0
    return


def test_vdi_delete_unknown_is_noop(client, fast_aspects) -> None:
    """
        Deleting an unknown VDI succeeds as a no-op.
    """
    client.Vdi.delete(vdi_uuid="vdi-never-seen", aspects=fast_aspects)
    return


def test_vdi_delete_is_idempotent(client, fast_aspects) -> None:
    """
        Deleting the same VDI twice succeeds, the second time as a no-op.
    """
    _seed_sr_ref(client, fast_aspects)
    spec = XenVdiSpec(name_label="d1", sr_uuid="sr-uuid-1",
                      virtual_size=1024)
    vdi = client.Vdi.create(spec=spec, aspects=fast_aspects)
    client.Vdi.delete(vdi_uuid=vdi.uuid, aspects=fast_aspects)
    client.Vdi.delete(vdi_uuid=vdi.uuid, aspects=fast_aspects)
    return


def test_vdi_resize_updates_virtual_size(client, transport,
                                         fast_aspects) -> None:
    """
        Vdi.resize updates the VDI virtual_size on the host.
    """
    _seed_sr_ref(client, fast_aspects)
    spec = XenVdiSpec(name_label="d1", sr_uuid="sr-uuid-1",
                      virtual_size=1024)
    vdi = client.Vdi.create(spec=spec, aspects=fast_aspects)
    client.Vdi.resize(vdi_uuid=vdi.uuid, size_bytes=4096,
                      aspects=fast_aspects)
    assert transport.vdis[vdi.uuid]["virtual_size"] == 4096
    return
