"""
    .. module:: test_snapshots
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: VM snapshot create/list/revert/destroy tests for the
        Snapshots api-group.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from ccai.interop.xen.model.xenvmsnapshot import XenVmSnapshot
from ccai.interop.xen.specs.xenvmclonespec import XenVmCloneSpec

from ccai import testbase
from .factories import (create_xen_client, create_xen_transport)


def _vm(client, fast_aspects):
    """
        Clone a VM and return its uuid.
    """
    client.Templates.list(aspects=fast_aspects)
    vm, _ = client.Vms.clone_from_template(
        template_uuid="tmpl-uuid-1",
        spec=XenVmCloneSpec(name_label="snap-vm"), aspects=fast_aspects)
    rtnval = vm.uuid
    return rtnval


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_snapshot_vm_returns_typed_record(transport, client, fast_aspects) -> None:
    """
        Snapshots.snapshot_vm takes a snapshot and returns a typed record.
    """
    vm_uuid = _vm(client, fast_aspects)
    snap = client.Snapshots.snapshot_vm(vm_uuid=vm_uuid, name="snap-1",
                                        aspects=fast_aspects)
    assert isinstance(snap, XenVmSnapshot)
    assert snap.name_label == "snap-1"
    assert snap.snapshot_of_uuid == vm_uuid
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_snapshots_list_for_vm(transport, client, fast_aspects) -> None:
    """
        Snapshots.list returns snapshots taken of a specific VM.
    """
    vm_uuid = _vm(client, fast_aspects)
    client.Snapshots.snapshot_vm(vm_uuid=vm_uuid, name="snap-1",
                                 aspects=fast_aspects)
    client.Snapshots.snapshot_vm(vm_uuid=vm_uuid, name="snap-2",
                                 aspects=fast_aspects)
    snapshots = client.Snapshots.list(vm_uuid=vm_uuid, aspects=fast_aspects)
    assert len(snapshots) == 2
    labels = sorted(s.name_label for s in snapshots)
    assert labels == ["snap-1", "snap-2"]
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_snapshots_list_excludes_other_vms(transport, client, fast_aspects) -> None:
    """
        Snapshots.list returns nothing for a VM with no snapshots.
    """
    _vm(client, fast_aspects)
    snapshots = client.Snapshots.list(vm_uuid="vm-other",
                                      aspects=fast_aspects)
    assert len(snapshots) == 0
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_snapshot_revert(transport, client, fast_aspects) -> None:
    """
        Snapshots.revert dispatches VM.revert without raising.
    """
    vm_uuid = _vm(client, fast_aspects)
    snap = client.Snapshots.snapshot_vm(vm_uuid=vm_uuid, name="snap-1",
                                        aspects=fast_aspects)
    client.Snapshots.revert(snapshot_uuid=snap.uuid, aspects=fast_aspects)
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_snapshot_destroy_is_idempotent(transport, client, fast_aspects) -> None:
    """
        Snapshots.destroy removes a snapshot; destroy is idempotent.
    """
    vm_uuid = _vm(client, fast_aspects)
    snap = client.Snapshots.snapshot_vm(vm_uuid=vm_uuid, name="snap-1",
                                        aspects=fast_aspects)
    client.Snapshots.destroy(snapshot_uuid=snap.uuid, aspects=fast_aspects)
    assert len(client.Snapshots.list(vm_uuid=vm_uuid,
                                     aspects=fast_aspects)) == 0
    client.Snapshots.destroy(snapshot_uuid=snap.uuid, aspects=fast_aspects)
    client.Snapshots.destroy(snapshot_uuid="snap-absent",
                             aspects=fast_aspects)
    return
