"""
    .. module:: test_attachments
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: VBD and VIF attach/detach tests for the Vbds and Vifs
        api-groups.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from ccai.interop.xen.model.xenvbd import XenVbd
from ccai.interop.xen.model.xenvif import XenVif
from ccai.interop.xen.specs.xenvbdspec import XenVbdSpec
from ccai.interop.xen.specs.xenvdispec import XenVdiSpec
from ccai.interop.xen.specs.xenvifspec import XenVifSpec
from ccai.interop.xen.specs.xenvmclonespec import XenVmCloneSpec

from ccai import testbase
from .factories import (create_xen_client, create_xen_transport)


def _vm_and_vdi(client, fast_aspects):
    """
        Clone a VM and create a VDI, returning their uuids.
    """
    client.Templates.list(aspects=fast_aspects)
    vm, _ = client.Vms.clone_from_template(
        template_uuid="tmpl-uuid-1",
        spec=XenVmCloneSpec(name_label="attach-vm"), aspects=fast_aspects)
    client.Sr.list(aspects=fast_aspects)
    vdi = client.Vdi.create(
        spec=XenVdiSpec(name_label="attach-vdi", sr_uuid="sr-uuid-1",
                        virtual_size=1024), aspects=fast_aspects)
    rtnval = (vm.uuid, vdi.uuid)
    return rtnval


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vbd_attach_returns_typed_record(transport, client, fast_aspects) -> None:
    """
        Vbds.attach links a VDI to a VM and returns a typed XenVbd.
    """
    vm_uuid, vdi_uuid = _vm_and_vdi(client, fast_aspects)
    vbd = client.Vbds.attach(
        spec=XenVbdSpec(vm_uuid=vm_uuid, vdi_uuid=vdi_uuid, userdevice="1"),
        aspects=fast_aspects)
    assert isinstance(vbd, XenVbd)
    assert vbd.vm_uuid == vm_uuid
    assert vbd.vdi_uuid == vdi_uuid
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vbd_attach_is_idempotent(transport, client, fast_aspects) -> None:
    """
        Attaching the same VM/VDI pair twice returns the existing VBD.
    """
    vm_uuid, vdi_uuid = _vm_and_vdi(client, fast_aspects)
    spec = XenVbdSpec(vm_uuid=vm_uuid, vdi_uuid=vdi_uuid, userdevice="1")
    first = client.Vbds.attach(spec=spec, aspects=fast_aspects)
    second = client.Vbds.attach(spec=spec, aspects=fast_aspects)
    assert first.uuid == second.uuid
    assert len(client.Vbds.list(vm_uuid=vm_uuid, aspects=fast_aspects)) == 1
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vbd_detach_removes_record(transport, client, fast_aspects) -> None:
    """
        Vbds.detach destroys a VBD; detach is idempotent.
    """
    vm_uuid, vdi_uuid = _vm_and_vdi(client, fast_aspects)
    vbd = client.Vbds.attach(
        spec=XenVbdSpec(vm_uuid=vm_uuid, vdi_uuid=vdi_uuid, userdevice="1"),
        aspects=fast_aspects)
    client.Vbds.detach(vbd_uuid=vbd.uuid, aspects=fast_aspects)
    assert len(client.Vbds.list(aspects=fast_aspects)) == 0
    client.Vbds.detach(vbd_uuid=vbd.uuid, aspects=fast_aspects)
    client.Vbds.detach(vbd_uuid="vbd-absent", aspects=fast_aspects)
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vif_attach_returns_typed_record(transport, client, fast_aspects) -> None:
    """
        Vifs.attach links a VM to a network and returns a typed XenVif.
    """
    vm_uuid, _ = _vm_and_vdi(client, fast_aspects)
    client.Networks.list(aspects=fast_aspects)
    vif = client.Vifs.attach(
        spec=XenVifSpec(vm_uuid=vm_uuid, network_uuid="net-uuid-1",
                        device="0"), aspects=fast_aspects)
    assert isinstance(vif, XenVif)
    assert vif.vm_uuid == vm_uuid
    assert vif.network_uuid == "net-uuid-1"
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vif_attach_is_idempotent(transport, client, fast_aspects) -> None:
    """
        Attaching the same VM/network/device triple twice returns the
        existing VIF.
    """
    vm_uuid, _ = _vm_and_vdi(client, fast_aspects)
    client.Networks.list(aspects=fast_aspects)
    spec = XenVifSpec(vm_uuid=vm_uuid, network_uuid="net-uuid-1",
                      device="0")
    first = client.Vifs.attach(spec=spec, aspects=fast_aspects)
    second = client.Vifs.attach(spec=spec, aspects=fast_aspects)
    assert first.uuid == second.uuid
    assert len(client.Vifs.list(vm_uuid=vm_uuid, aspects=fast_aspects)) == 1
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vif_detach_removes_record(transport, client, fast_aspects) -> None:
    """
        Vifs.detach destroys a VIF; detach is idempotent.
    """
    vm_uuid, _ = _vm_and_vdi(client, fast_aspects)
    client.Networks.list(aspects=fast_aspects)
    vif = client.Vifs.attach(
        spec=XenVifSpec(vm_uuid=vm_uuid, network_uuid="net-uuid-1",
                        device="0"), aspects=fast_aspects)
    client.Vifs.detach(vif_uuid=vif.uuid, aspects=fast_aspects)
    assert len(client.Vifs.list(aspects=fast_aspects)) == 0
    client.Vifs.detach(vif_uuid=vif.uuid, aspects=fast_aspects)
    client.Vifs.detach(vif_uuid="vif-absent", aspects=fast_aspects)
    return
