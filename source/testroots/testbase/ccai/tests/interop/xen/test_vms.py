"""
    .. module:: test_vms
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: VM clone-from-template, lifecycle and enumeration tests for
        the Vms api-group.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from ccai import testbase


from ccai.interop.xen.model.xentaskhandle import XenTaskHandle
from ccai.interop.xen.model.xenvm import XenVm
from ccai.interop.xen.specs.xenvmclonespec import XenVmCloneSpec

from ccai.tests.interop.xen.factories import (create_xen_client, create_xen_transport)


def _clone(client, fast_aspects, *, name_label="worker-01",
           vcpus_max=None, memory_bytes=None, other_config=None,
           tags=None, xenstore_data=None):
    """
        Enumerate templates then clone a VM, returning ``(vm, handle)``.
    """
    client.Templates.list(aspects=fast_aspects)
    spec = XenVmCloneSpec(
        name_label=name_label, name_description="cloned by test",
        vcpus_max=vcpus_max, memory_bytes=memory_bytes,
        other_config=other_config if other_config is not None else {},
        tags=tags if tags is not None else [],
        xenstore_data=xenstore_data if xenstore_data is not None else {},
    )
    rtnval = client.Vms.clone_from_template(template_uuid="tmpl-uuid-1",
                                            spec=spec, aspects=fast_aspects)
    return rtnval


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_clone_from_template_returns_vm_and_handle(transport, client,
                                                   fast_aspects) -> None:
    """
        Cloning yields a typed XenVm and a provision XenTaskHandle.
    """
    vm, handle = _clone(client, fast_aspects)
    assert isinstance(vm, XenVm)
    assert vm.name_label == "worker-01"
    assert vm.is_a_template is False
    assert isinstance(handle, XenTaskHandle)
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_clone_applies_overrides(transport, client, fast_aspects) -> None:
    """
        Clone applies vcpu / memory / other_config / tags / xenstore data.
    """
    vm, _ = _clone(client, fast_aspects, vcpus_max=4,
                   memory_bytes=8589934592,
                   other_config={"owner": "qa"}, tags=["batch"],
                   xenstore_data={"vm-data/cloud-init": "payload"})
    record = transport.vms[vm.uuid]
    assert record["VCPUs_max"] == 4
    assert record["memory_static_max"] == 8589934592
    assert record["other_config"]["owner"] == "qa"
    assert "batch" in record["tags"]
    assert record["xenstore_data"]["vm-data/cloud-init"] == "payload"
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_clone_is_idempotent_by_name_label(transport, client, fast_aspects) -> None:
    """
        Re-cloning with an existing name_label returns the existing VM and
        a None task handle.
    """
    first_vm, first_handle = _clone(client, fast_aspects)
    second_vm, second_handle = _clone(client, fast_aspects)
    assert first_vm.uuid == second_vm.uuid
    assert second_handle is None
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_provision_task_handle_completes(transport, client, fast_aspects) -> None:
    """
        The provision task handle waits to a SUCCEEDED terminal state.
    """
    _, handle = _clone(client, fast_aspects)
    result = handle.wait(aspects=fast_aspects)
    assert result.state.name == "SUCCEEDED"
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vms_list_excludes_templates(transport, client, fast_aspects) -> None:
    """
        Vms.list returns cloned VMs but not templates.
    """
    _clone(client, fast_aspects)
    vms = client.Vms.list(aspects=fast_aspects)
    assert len(vms) == 1
    assert vms[0].name_label == "worker-01"
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vms_get_by_uuid(transport, client, fast_aspects) -> None:
    """
        Vms.get returns a XenVm for a known uuid and None for an unknown.
    """
    vm, _ = _clone(client, fast_aspects)
    fetched = client.Vms.get(vm_uuid=vm.uuid, aspects=fast_aspects)
    assert fetched is not None
    assert fetched.uuid == vm.uuid

    missing = client.Vms.get(vm_uuid="vm-absent", aspects=fast_aspects)
    assert missing is None
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vms_get_by_name_label(transport, client, fast_aspects) -> None:
    """
        Vms.get_by_name_label finds a cloned VM and misses absent ones.
    """
    _clone(client, fast_aspects)
    found = client.Vms.get_by_name_label(name_label="worker-01",
                                         aspects=fast_aspects)
    assert found is not None
    none_found = client.Vms.get_by_name_label(name_label="absent",
                                              aspects=fast_aspects)
    assert none_found is None
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
@testbase.parametrize("operation,expected_state", [
    ("start", "Running"),
    ("clean_shutdown", "Halted"),
    ("hard_shutdown", "Halted"),
    ("reboot", "Running"),
    ("suspend", "Suspended"),
    ("resume", "Running"),
])
def test_vm_power_operations(transport, client, fast_aspects, operation,
                             expected_state) -> None:
    """
        Each VM power op dispatches an Async task and moves power state.
    """
    vm, _ = _clone(client, fast_aspects)
    op = getattr(client.Vms, operation)
    handle = op(vm_uuid=vm.uuid, aspects=fast_aspects)
    assert isinstance(handle, XenTaskHandle)
    assert transport.vms[vm.uuid]["power_state"] == expected_state
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vm_wait_for_power_state(transport, client, fast_aspects) -> None:
    """
        wait_for_power_state returns once the VM reaches the desired state.
    """
    vm, _ = _clone(client, fast_aspects)
    client.Vms.start(vm_uuid=vm.uuid, aspects=fast_aspects)
    client.Vms.wait_for_power_state(vm_uuid=vm.uuid,
                                    desired_state="Running",
                                    aspects=fast_aspects)
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vm_destroy_removes_record(transport, client, fast_aspects) -> None:
    """
        Vms.destroy removes the VM by uuid.
    """
    vm, _ = _clone(client, fast_aspects)
    client.Vms.destroy(vm_uuid=vm.uuid, aspects=fast_aspects)
    assert len(client.Vms.list(aspects=fast_aspects)) == 0
    return


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_vm_destroy_is_idempotent(transport, client, fast_aspects) -> None:
    """
        Destroying a VM twice (and an unknown VM) succeeds as a no-op.
    """
    vm, _ = _clone(client, fast_aspects)
    client.Vms.destroy(vm_uuid=vm.uuid, aspects=fast_aspects)
    client.Vms.destroy(vm_uuid=vm.uuid, aspects=fast_aspects)
    client.Vms.destroy(vm_uuid="vm-never-seen", aspects=fast_aspects)
    return
