"""
    .. module:: vmsgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: VmsGroup — XAPI VM clone-from-template, lifecycle and
        enumeration.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import Any, Callable, List, Optional, Tuple

from ccai.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from ccai.interop.xen.apigroups.basegroup import BaseGroup
from ccai.interop.xen.exceptions.xenexceptions import is_handle_invalid, XenError
from ccai.interop.xen.model.xentaskhandle import XenTaskHandle
from ccai.interop.xen.model.xenvm import XenVm
from ccai.interop.xen.refs.refresolver import RefResolver
from ccai.interop.xen.session.xensessionmanager import XenSessionManager
from ccai.interop.xen.specs.xenvmclonespec import XenVmCloneSpec


def _record_to_vm(*, record: Any, resolver: RefResolver) -> XenVm:
    """
        Convert an XAPI VM record dict to a :class:`XenVm`.

        :param record: The XAPI VM record dict.
        :param resolver: The shared RefResolver (unused; kept for symmetry).

        :returns: A :class:`XenVm` record.
    """
    _ = resolver
    other_config = record.get("other_config", {})
    if not isinstance(other_config, dict):
        other_config = {}
    tags = record.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    rtnval = XenVm(
        uuid=record.get("uuid", ""),
        name_label=record.get("name_label", ""),
        name_description=record.get("name_description", ""),
        power_state=record.get("power_state", "Halted"),
        vcpus_max=int(record.get("VCPUs_max", record.get("vcpus_max", 1))),
        memory_static_max=int(record.get("memory_static_max", 0)),
        is_a_template=bool(record.get("is_a_template", False)),
        is_control_domain=bool(record.get("is_control_domain", False)),
        other_config=dict(other_config),
        tags=list(tags),
    )
    return rtnval


class VmsGroup(BaseGroup):
    """
        XAPI ``VM`` object-class operations.

        Covers clone-from-template (with read-before-create), the power
        lifecycle (start / clean-shutdown / hard-shutdown / reboot / suspend
        / resume), idempotent destroy, and typed enumeration.  Async
        operations that XAPI exposes through ``Async.*`` return a
        :class:`XenTaskHandle`.
    """

    def __init__(self, *, session_manager: XenSessionManager,
                 resolver: RefResolver,
                 task_handle_factory: Callable[[str], XenTaskHandle]) -> None:
        """
            Construct a VmsGroup.

            :param session_manager: The shared XenSessionManager.
            :param resolver: The shared RefResolver.
            :param task_handle_factory: Callable turning a task uuid into a
                                        :class:`XenTaskHandle`.
        """
        super().__init__(session_manager=session_manager, resolver=resolver)
        self._task_handle_factory: Callable[[str], XenTaskHandle] = (
            task_handle_factory)
        return

    # ------------------------------------------------------------------
    # Enumeration
    # ------------------------------------------------------------------

    def list(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
             ) -> List[XenVm]:
        """
            Enumerate non-template, non-control-domain VMs.

            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenVm` records.
        """
        records = self._call(method_path="VM.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenVm] = []
        if isinstance(records, dict):
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)
                if bool(record.get("is_a_template", False)) is True:
                    continue
                if bool(record.get("is_control_domain", False)) is True:
                    continue
                out.append(_record_to_vm(record=record,
                                         resolver=self._resolver))
        rtnval = out
        return rtnval

    def get(self, *, vm_uuid: str,
            aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
            ) -> Optional[XenVm]:
        """
            Return the :class:`XenVm` for a uuid, or None when absent.

            :param vm_uuid: The VM uuid.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenVm` record, or None.
        """
        try:
            vm_ref = self._call(method_path="VM.get_by_uuid",
                                args=[vm_uuid], aspects=aspects)
        except XenError:
            rtnval = None
            return rtnval

        record = self._call(method_path="VM.get_record", args=[vm_ref],
                             aspects=aspects)
        self._record_ref(opaque_ref=vm_ref, record=record)
        rtnval = _record_to_vm(record=record, resolver=self._resolver)
        return rtnval

    def get_by_name_label(self, *, name_label: str,
                          aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                          ) -> Optional[XenVm]:
        """
            Return the first non-template VM with a matching name_label.

            :param name_label: The VM name_label to match.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenVm` record, or None.
        """
        for vm in self.list(aspects=aspects):
            if vm.name_label == name_label:
                rtnval = vm
                return rtnval
        rtnval = None
        return rtnval

    # ------------------------------------------------------------------
    # Clone-from-template
    # ------------------------------------------------------------------

    def clone_from_template(self, *, template_uuid: str,
                            spec: XenVmCloneSpec,
                            aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                            ) -> Tuple[XenVm, Optional[XenTaskHandle]]:
        """
            Clone a VM from a template and apply the spec's overrides.

            Performs ``VM.clone``, applies the memory / vCPU / other_config /
            tags / xenstore overrides, then ``VM.provision``.  When a VM with
            the same ``name_label`` already exists, the existing record is
            returned (read-before-create) with a ``None`` task handle.

            :param template_uuid: The uuid of the template to clone.
            :param spec: The :class:`XenVmCloneSpec` of overrides.
            :param aspects: Behaviour controls.

            :returns: A tuple ``(XenVm, Optional[XenTaskHandle])``.
        """
        existing = self.get_by_name_label(name_label=spec.name_label,
                                           aspects=aspects)
        if existing is not None:
            rtnval = (existing, None)
            return rtnval

        template_ref = self._resolver.ref_for(uuid=template_uuid)

        task_uuid = self._call(method_path="Async.VM.clone",
                               args=[template_ref, spec.name_label],
                               aspects=aspects)
        clone_handle = self._task_handle_factory(task_uuid)
        clone_result = clone_handle.wait(aspects=aspects)
        clone_ref = None
        if clone_result.payload is not None:
            clone_ref = clone_result.payload.get("result", None)
        if clone_ref is None:
            clone_ref = self._call(method_path="VM.get_by_name_label",
                                   args=[spec.name_label], aspects=aspects)
            if isinstance(clone_ref, list) and len(clone_ref) > 0:
                clone_ref = clone_ref[0]

        # Apply overrides.
        if spec.name_description is not None and len(
                spec.name_description) > 0:
            self._call(method_path="VM.set_name_description",
                       args=[clone_ref, spec.name_description],
                       aspects=aspects)
        if spec.vcpus_max is not None:
            self._call(method_path="VM.set_VCPUs_max",
                       args=[clone_ref, str(spec.vcpus_max)],
                       aspects=aspects)
            self._call(method_path="VM.set_VCPUs_at_startup",
                       args=[clone_ref, str(spec.vcpus_max)],
                       aspects=aspects)
        if spec.memory_bytes is not None:
            mem = str(spec.memory_bytes)
            self._call(method_path="VM.set_memory_limits",
                       args=[clone_ref, mem, mem, mem, mem],
                       aspects=aspects)
        for key, value in spec.other_config.items():
            self._call(method_path="VM.add_to_other_config",
                       args=[clone_ref, key, value], aspects=aspects)
        for tag in spec.tags:
            self._call(method_path="VM.add_tags", args=[clone_ref, tag],
                       aspects=aspects)
        for key, value in spec.xenstore_data.items():
            self._call(method_path="VM.add_to_xenstore_data",
                       args=[clone_ref, key, value], aspects=aspects)

        provision_handle: Optional[XenTaskHandle] = None
        provision_task = self._call(method_path="Async.VM.provision",
                                    args=[clone_ref], aspects=aspects)
        if provision_task is not None:
            provision_handle = self._task_handle_factory(provision_task)

        record = self._call(method_path="VM.get_record", args=[clone_ref],
                             aspects=aspects)
        self._record_ref(opaque_ref=clone_ref, record=record)
        vm = _record_to_vm(record=record, resolver=self._resolver)

        rtnval = (vm, provision_handle)
        return rtnval

    # ------------------------------------------------------------------
    # Power lifecycle
    # ------------------------------------------------------------------

    def _power_op(self, *, vm_uuid: str, async_method: str,
                  extra_args: Optional[List[Any]],
                  aspects: AspectsXapi) -> Optional[XenTaskHandle]:
        """
            Dispatch an ``Async.VM.*`` power op and wrap the task.

            :param vm_uuid: The target VM uuid.
            :param async_method: The dotted ``Async.VM.*`` method path.
            :param extra_args: Optional extra positional arguments.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenTaskHandle`, or None.
        """
        vm_ref = self._resolver.ref_for(uuid=vm_uuid)
        call_args: List[Any] = [vm_ref]
        if extra_args is not None:
            call_args.extend(extra_args)
        task_uuid = self._call(method_path=async_method, args=call_args,
                               aspects=aspects)
        handle: Optional[XenTaskHandle] = None
        if task_uuid is not None:
            handle = self._task_handle_factory(task_uuid)
        rtnval = handle
        return rtnval

    def start(self, *, vm_uuid: str,
              aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
              ) -> Optional[XenTaskHandle]:
        """
            Start a halted VM.

            :param vm_uuid: The target VM uuid.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenTaskHandle`, or None.
        """
        rtnval = self._power_op(vm_uuid=vm_uuid,
                                async_method="Async.VM.start",
                                extra_args=[False, False], aspects=aspects)
        return rtnval

    def clean_shutdown(self, *, vm_uuid: str,
                       aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                       ) -> Optional[XenTaskHandle]:
        """
            Cleanly shut down a running VM.

            :param vm_uuid: The target VM uuid.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenTaskHandle`, or None.
        """
        rtnval = self._power_op(vm_uuid=vm_uuid,
                                async_method="Async.VM.clean_shutdown",
                                extra_args=None, aspects=aspects)
        return rtnval

    def hard_shutdown(self, *, vm_uuid: str,
                      aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                      ) -> Optional[XenTaskHandle]:
        """
            Forcibly power off a VM.

            :param vm_uuid: The target VM uuid.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenTaskHandle`, or None.
        """
        rtnval = self._power_op(vm_uuid=vm_uuid,
                                async_method="Async.VM.hard_shutdown",
                                extra_args=None, aspects=aspects)
        return rtnval

    def reboot(self, *, vm_uuid: str,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
               ) -> Optional[XenTaskHandle]:
        """
            Cleanly reboot a running VM.

            :param vm_uuid: The target VM uuid.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenTaskHandle`, or None.
        """
        rtnval = self._power_op(vm_uuid=vm_uuid,
                                async_method="Async.VM.clean_reboot",
                                extra_args=None, aspects=aspects)
        return rtnval

    def suspend(self, *, vm_uuid: str,
                aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                ) -> Optional[XenTaskHandle]:
        """
            Suspend a running VM.

            :param vm_uuid: The target VM uuid.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenTaskHandle`, or None.
        """
        rtnval = self._power_op(vm_uuid=vm_uuid,
                                async_method="Async.VM.suspend",
                                extra_args=None, aspects=aspects)
        return rtnval

    def resume(self, *, vm_uuid: str,
               aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
               ) -> Optional[XenTaskHandle]:
        """
            Resume a suspended VM.

            :param vm_uuid: The target VM uuid.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenTaskHandle`, or None.
        """
        rtnval = self._power_op(vm_uuid=vm_uuid,
                                async_method="Async.VM.resume",
                                extra_args=[False, False], aspects=aspects)
        return rtnval

    def destroy(self, *, vm_uuid: str,
                aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Destroy a VM by uuid.

            Idempotent: destroying an unknown VM succeeds as a no-op.

            :param vm_uuid: The uuid of the VM to destroy.
            :param aspects: Behaviour controls.
        """
        vm_ref = self._resolver.maybe_ref_for(uuid=vm_uuid)
        if vm_ref is None:
            # An unknown uuid has no live VM to destroy; this is a no-op.
            return

        try:
            self._call(method_path="VM.destroy", args=[vm_ref],
                       aspects=aspects)
        except XenError as xerr:
            # Only an already-absent handle makes destroy a no-op; any other XAPI
            # fault (in-use, not-allowed, permission) is a genuine failure.
            if not is_handle_invalid(xerr):
                raise
        self._resolver.forget_uuid(uuid=vm_uuid)
        return

    def wait_for_power_state(self, *, vm_uuid: str, desired_state: str,
                             aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                             ) -> None:
        """
            Poll a VM until it reaches the desired power state.

            :param vm_uuid: The target VM uuid.
            :param desired_state: The XAPI power state to wait for.
            :param aspects: Behaviour controls; drives the poll loop.

            :raises: TimeoutError
        """
        import os
        import time

        vm_ref = self._resolver.ref_for(uuid=vm_uuid)
        started = time.monotonic()
        timeout = aspects.completion_timeout
        interval = aspects.completion_interval

        while True:
            current = self._call(method_path="VM.get_power_state",
                                 args=[vm_ref], aspects=aspects)
            if current == desired_state:
                return

            elapsed = time.monotonic() - started
            if elapsed > timeout:
                err_msg_lines = ["VM did not reach the desired power state."]
                err_msg_lines.append("VM: {}".format(vm_uuid))
                err_msg_lines.append("DESIRED: {}".format(desired_state))
                err_msg_lines.append("CURRENT: {}".format(current))
                err_msg_lines.append("TIMEOUT: {}s".format(timeout))
                err_msg = os.linesep.join(err_msg_lines)
                raise TimeoutError(err_msg)

            time.sleep(interval)
