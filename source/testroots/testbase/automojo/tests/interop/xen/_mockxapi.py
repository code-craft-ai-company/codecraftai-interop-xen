"""
    .. module:: _mockxapi
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: MockXapiTransport — an in-memory stand-in for the XAPI
        XML-RPC transport, returning deterministic ``Status``/``Value``
        envelopes so the Xen client can be exercised without a real host.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import Any, Callable, Dict, List, Optional


def _ok(value: Any) -> Dict[str, Any]:
    """
        Wrap a value in an XAPI success envelope.

        :param value: The payload value.

        :returns: A ``{"Status": "Success", "Value": value}`` dict.
    """
    rtnval = {"Status": "Success", "Value": value}
    return rtnval


def _fail(*codes: str) -> Dict[str, Any]:
    """
        Build an XAPI failure envelope.

        :param codes: The XAPI ``ErrorDescription`` codes.

        :returns: A failure envelope dict.
    """
    rtnval = {"Status": "Failure", "ErrorDescription": list(codes)}
    return rtnval


class _MethodProxy:
    """
        Dotted-path proxy resolving ``transport.VM.get_all_records`` style
        access onto the owning transport's dispatch function.
    """

    def __init__(self, *, path: str,
                 dispatch: Callable[[str, tuple], Any]) -> None:
        """
            Construct a _MethodProxy.

            :param path: The dotted method path accumulated so far.
            :param dispatch: The transport dispatch callable.
        """
        self._path: str = path
        self._dispatch: Callable[[str, tuple], Any] = dispatch
        return

    def __getattr__(self, name: str) -> "_MethodProxy":
        """
            Extend the dotted path by one segment.

            :param name: The next path segment.

            :returns: A deeper :class:`_MethodProxy`.
        """
        deeper = "{}.{}".format(self._path, name) if len(self._path) > 0 else name
        rtnval = _MethodProxy(path=deeper, dispatch=self._dispatch)
        return rtnval

    def __call__(self, *args: Any) -> Any:
        """
            Invoke the accumulated method path.

            :param args: The XML-RPC positional arguments.

            :returns: The dispatch result.
        """
        rtnval = self._dispatch(self._path, args)
        return rtnval


class MockXapiTransport:
    """
        In-memory mock of the XAPI XML-RPC transport.

        Models a tiny pool: one pool, one host, one network, one SR, a
        configurable template set, and dictionaries tracking created VMs,
        VDIs, VBDs, VIFs and tasks.  Every call is recorded in ``calls``.

        The transport may be told to fail the next ``session_invalid_after``
        non-session call with ``SESSION_INVALID`` so transparent-re-login
        behaviour can be exercised.
    """

    def __init__(self, *, templates: Optional[Dict[str, str]] = None,
                 reject_login: bool = False) -> None:
        """
            Construct a MockXapiTransport.

            :param templates: Mapping ``template_uuid -> name_label`` of
                              templates that exist in the pool.
            :param reject_login: When True, ``login_with_password`` fails.
        """
        self._reject_login: bool = reject_login
        self.calls: List[str] = []
        self._session_counter: int = 0
        self._ref_counter: int = 0
        self._login_count: int = 0

        # SESSION_INVALID injection: fail the Nth dispatched non-session call.
        self.session_invalid_on_call: Optional[int] = None
        self._non_session_calls: int = 0

        templates = templates if templates is not None else {
            "tmpl-uuid-1": "Ubuntu 22.04 Template"}

        self.session = _MethodProxy(path="session",
                                    dispatch=self._dispatch_session)

        # Object stores keyed by uuid; opaque refs are uuid-prefixed.
        self.pools: Dict[str, Dict[str, Any]] = {
            "pool-uuid-1": {"uuid": "pool-uuid-1",
                            "name_label": "homelab-pool",
                            "name_description": "",
                            "master": "OpaqueRef:host-uuid-1"}}
        self.hosts: Dict[str, Dict[str, Any]] = {
            "host-uuid-1": {"uuid": "host-uuid-1", "name_label": "xen-host-1",
                            "address": "10.0.0.10", "enabled": True}}
        self.networks: Dict[str, Dict[str, Any]] = {
            "net-uuid-1": {"uuid": "net-uuid-1", "name_label": "Pool-wide "
                           "network associated with eth0",
                           "name_description": "", "bridge": "xenbr0",
                           "MTU": 1500}}
        self.pifs: Dict[str, Dict[str, Any]] = {
            "pif-uuid-1": {"uuid": "pif-uuid-1", "device": "eth0",
                           "host": "OpaqueRef:host-uuid-1",
                           "network": "OpaqueRef:net-uuid-1",
                           "management": True}}
        self.srs: Dict[str, Dict[str, Any]] = {
            "sr-uuid-1": {"uuid": "sr-uuid-1", "name_label": "Local storage",
                          "type": "ext", "physical_size": 1099511627776,
                          "physical_utilisation": 107374182400,
                          "shared": False}}
        self.vdis: Dict[str, Dict[str, Any]] = {}
        self.vbds: Dict[str, Dict[str, Any]] = {}
        self.vifs: Dict[str, Dict[str, Any]] = {}
        self.tasks: Dict[str, Dict[str, Any]] = {}

        self.vms: Dict[str, Dict[str, Any]] = {}
        for tmpl_uuid, tmpl_name in templates.items():
            self.vms[tmpl_uuid] = {
                "uuid": tmpl_uuid, "name_label": tmpl_name,
                "name_description": "", "power_state": "Halted",
                "VCPUs_max": 1, "memory_static_max": 1073741824,
                "is_a_template": True, "is_control_domain": False,
                "is_a_snapshot": False, "other_config": {}, "tags": [],
            }

        # Dispatch table keyed by dotted XAPI method path.
        self._top = _MethodProxy(path="", dispatch=self._dispatch_xapi)
        return

    @property
    def login_count(self) -> int:
        """
            Return the number of successful logins performed.

            :returns: The login counter.
        """
        rtnval = self._login_count
        return rtnval

    def __getattr__(self, name: str) -> Any:
        """
            Resolve ``transport.<ObjectClass>`` onto a dispatching proxy.

            Internal attribute lookups (dunder names and ``_op_*`` handler
            probes that miss) must raise :class:`AttributeError` so a missing
            handler is reported by the dispatcher rather than turning into an
            infinite ``__getattr__`` recursion.

            :param name: The object-class segment (VM, VDI, ...).

            :returns: A :class:`_MethodProxy`.
            :raises: AttributeError
        """
        if name.startswith("_"):
            err_msg = "MockXapiTransport has no attribute {!r}.".format(name)
            raise AttributeError(err_msg)
        rtnval = _MethodProxy(path=name, dispatch=self._dispatch_xapi)
        return rtnval

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _ref(self, *, uuid: str) -> str:
        """
            Build the deterministic opaque ref for a uuid.

            :param uuid: The object uuid.

            :returns: The opaque ref string.
        """
        rtnval = "OpaqueRef:{}".format(uuid)
        return rtnval

    @staticmethod
    def _uuid_of(*, opaque_ref: str) -> str:
        """
            Extract the uuid from a deterministic opaque ref.

            :param opaque_ref: The opaque ref string.

            :returns: The uuid.
        """
        rtnval = opaque_ref.split(":", 1)[1]
        return rtnval

    def _alloc(self, *, prefix: str) -> str:
        """
            Allocate a deterministic uuid.

            :param prefix: The uuid prefix.

            :returns: A unique uuid string.
        """
        self._ref_counter = self._ref_counter + 1
        rtnval = "{}-uuid-{}".format(prefix, self._ref_counter)
        return rtnval

    def _records_envelope(self, *, store: Dict[str, Dict[str, Any]]
                          ) -> Dict[str, Any]:
        """
            Build a ``get_all_records`` envelope keyed by opaque ref.

            :param store: The object store dict keyed by uuid.

            :returns: A success envelope whose value maps opaque ref to
                      record.
        """
        out: Dict[str, Any] = {}
        for uuid, record in store.items():
            out[self._ref(uuid=uuid)] = record
        rtnval = _ok(out)
        return rtnval

    # ------------------------------------------------------------------
    # session.* dispatch
    # ------------------------------------------------------------------

    def _dispatch_session(self, method_path: str, args: tuple) -> Any:
        """
            Dispatch a ``session.*`` call.

            :param method_path: The dotted method path.
            :param args: The XML-RPC positional arguments.

            :returns: An XAPI envelope.
        """
        self.calls.append(method_path)
        leaf = method_path.split(".")[-1]

        if leaf == "login_with_password":
            if self._reject_login is True:
                return _fail("SESSION_AUTHENTICATION_FAILED")
            self._session_counter = self._session_counter + 1
            self._login_count = self._login_count + 1
            rtnval = _ok("OpaqueRef:session-{}".format(self._session_counter))
            return rtnval

        if leaf == "logout":
            rtnval = _ok(None)
            return rtnval

        rtnval = _fail("MESSAGE_METHOD_UNKNOWN", method_path)
        return rtnval

    # ------------------------------------------------------------------
    # XAPI object dispatch
    # ------------------------------------------------------------------

    def _dispatch_xapi(self, method_path: str, args: tuple) -> Any:
        """
            Dispatch an XAPI object-class call.

            The leading argument is the session ref; the remainder are XAPI
            positional arguments.

            :param method_path: The dotted method path.
            :param args: The XML-RPC positional arguments.

            :returns: An XAPI envelope.
        """
        self.calls.append(method_path)
        self._non_session_calls = self._non_session_calls + 1

        if (self.session_invalid_on_call is not None
                and self._non_session_calls == self.session_invalid_on_call):
            # One-shot injection: clear so the retry succeeds.
            self.session_invalid_on_call = None
            return _fail("SESSION_INVALID")

        rest = list(args[1:])
        handler_name = "_op_" + method_path.replace(".", "_")
        handler = getattr(self, handler_name, None)
        if handler is None:
            return _fail("MESSAGE_METHOD_UNKNOWN", method_path)
        rtnval = handler(rest)
        return rtnval

    # -- enumeration ops ----------------------------------------------

    def _op_pool_get_all_records(self, args: list) -> Any:
        """ Return all pool records. """
        return self._records_envelope(store=self.pools)

    def _op_host_get_all_records(self, args: list) -> Any:
        """ Return all host records. """
        return self._records_envelope(store=self.hosts)

    def _op_network_get_all_records(self, args: list) -> Any:
        """ Return all network records. """
        return self._records_envelope(store=self.networks)

    def _op_PIF_get_all_records(self, args: list) -> Any:
        """ Return all PIF records. """
        return self._records_envelope(store=self.pifs)

    def _op_SR_get_all_records(self, args: list) -> Any:
        """ Return all SR records. """
        return self._records_envelope(store=self.srs)

    def _op_VDI_get_all_records(self, args: list) -> Any:
        """ Return all VDI records. """
        return self._records_envelope(store=self.vdis)

    def _op_VM_get_all_records(self, args: list) -> Any:
        """ Return all VM records. """
        return self._records_envelope(store=self.vms)

    def _op_VBD_get_all_records(self, args: list) -> Any:
        """ Return all VBD records. """
        return self._records_envelope(store=self.vbds)

    def _op_VIF_get_all_records(self, args: list) -> Any:
        """ Return all VIF records. """
        return self._records_envelope(store=self.vifs)

    # -- VDI ops -------------------------------------------------------

    def _op_VDI_create(self, args: list) -> Any:
        """ Create a VDI from a record dict. """
        record = args[0]
        uuid = self._alloc(prefix="vdi")
        sr_uuid = self._uuid_of(opaque_ref=record["SR"])
        self.vdis[uuid] = {
            "uuid": uuid, "name_label": record["name_label"],
            "name_description": record.get("name_description", ""),
            "SR": record["SR"], "virtual_size": int(record["virtual_size"]),
        }
        return _ok(self._ref(uuid=uuid))

    def _op_VDI_get_uuid(self, args: list) -> Any:
        """ Return a VDI uuid for an opaque ref. """
        return _ok(self._uuid_of(opaque_ref=args[0]))

    def _op_VDI_destroy(self, args: list) -> Any:
        """ Destroy a VDI by ref. """
        uuid = self._uuid_of(opaque_ref=args[0])
        if uuid in self.vdis:
            del self.vdis[uuid]
            return _ok(None)
        return _fail("HANDLE_INVALID", "VDI", args[0])

    def _op_VDI_resize(self, args: list) -> Any:
        """ Resize a VDI. """
        uuid = self._uuid_of(opaque_ref=args[0])
        if uuid in self.vdis:
            self.vdis[uuid]["virtual_size"] = int(args[1])
        return _ok(None)

    # -- task ops ------------------------------------------------------

    def _op_task_get_by_uuid(self, args: list) -> Any:
        """ Return a task ref for a uuid. """
        return _ok(self._ref(uuid=args[0]))

    def _op_task_get_record(self, args: list) -> Any:
        """ Return a task record. """
        uuid = self._uuid_of(opaque_ref=args[0])
        record = self.tasks.get(uuid, None)
        if record is None:
            return _fail("HANDLE_INVALID", "task", args[0])
        return _ok(record)

    # -- VM lifecycle --------------------------------------------------

    def _make_task(self, *, status: str = "success",
                   result: Optional[str] = None) -> str:
        """
            Create a task record and return its uuid.

            :param status: The terminal task status.
            :param result: Optional task result ref.

            :returns: The task uuid.
        """
        uuid = self._alloc(prefix="task")
        self.tasks[uuid] = {"uuid": uuid, "status": status, "progress": 1.0,
                            "result": result, "error_info": []}
        return uuid

    def _op_Async_VM_clone(self, args: list) -> Any:
        """ Clone a VM from a template ref, returning a task uuid. """
        template_uuid = self._uuid_of(opaque_ref=args[0])
        name_label = args[1]
        template = self.vms[template_uuid]
        uuid = self._alloc(prefix="vm")
        self.vms[uuid] = {
            "uuid": uuid, "name_label": name_label, "name_description": "",
            "power_state": "Halted", "VCPUs_max": template["VCPUs_max"],
            "memory_static_max": template["memory_static_max"],
            "is_a_template": False, "is_control_domain": False,
            "is_a_snapshot": False, "other_config": {}, "tags": [],
            "xenstore_data": {},
        }
        task_uuid = self._make_task(status="success",
                                    result=self._ref(uuid=uuid))
        return _ok(task_uuid)

    def _op_VM_get_by_name_label(self, args: list) -> Any:
        """ Return refs of VMs with a matching name_label. """
        matches = [self._ref(uuid=u) for u, r in self.vms.items()
                   if r["name_label"] == args[0]]
        return _ok(matches)

    def _op_VM_get_by_uuid(self, args: list) -> Any:
        """ Return a VM ref for a uuid. """
        if args[0] in self.vms:
            return _ok(self._ref(uuid=args[0]))
        return _fail("UUID_INVALID", "VM", args[0])

    def _op_VM_get_record(self, args: list) -> Any:
        """ Return a VM record for a ref. """
        uuid = self._uuid_of(opaque_ref=args[0])
        record = self.vms.get(uuid, None)
        if record is None:
            return _fail("HANDLE_INVALID", "VM", args[0])
        return _ok(record)

    def _op_VM_get_power_state(self, args: list) -> Any:
        """ Return a VM power state. """
        uuid = self._uuid_of(opaque_ref=args[0])
        return _ok(self.vms[uuid]["power_state"])

    def _op_VM_set_name_description(self, args: list) -> Any:
        """ Set a VM name_description. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["name_description"] = args[1]
        return _ok(None)

    def _op_VM_set_VCPUs_max(self, args: list) -> Any:
        """ Set a VM VCPUs_max. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["VCPUs_max"] = int(args[1])
        return _ok(None)

    def _op_VM_set_VCPUs_at_startup(self, args: list) -> Any:
        """ Set a VM VCPUs_at_startup (no-op store). """
        return _ok(None)

    def _op_VM_set_memory_limits(self, args: list) -> Any:
        """ Set a VM memory limits. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["memory_static_max"] = int(
            args[4])
        return _ok(None)

    def _op_VM_add_to_other_config(self, args: list) -> Any:
        """ Add a key/value to a VM other_config. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["other_config"][
            args[1]] = args[2]
        return _ok(None)

    def _op_VM_add_tags(self, args: list) -> Any:
        """ Add a tag to a VM. """
        record = self.vms[self._uuid_of(opaque_ref=args[0])]
        if args[1] not in record["tags"]:
            record["tags"].append(args[1])
        return _ok(None)

    def _op_VM_add_to_xenstore_data(self, args: list) -> Any:
        """ Add a key/value to a VM xenstore_data. """
        record = self.vms[self._uuid_of(opaque_ref=args[0])]
        record.setdefault("xenstore_data", {})[args[1]] = args[2]
        return _ok(None)

    def _op_Async_VM_provision(self, args: list) -> Any:
        """ Provision a cloned VM, returning a task uuid. """
        return _ok(self._make_task(status="success"))

    def _op_Async_VM_start(self, args: list) -> Any:
        """ Start a VM, returning a task uuid. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["power_state"] = "Running"
        return _ok(self._make_task(status="success"))

    def _op_Async_VM_clean_shutdown(self, args: list) -> Any:
        """ Cleanly shut down a VM, returning a task uuid. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["power_state"] = "Halted"
        return _ok(self._make_task(status="success"))

    def _op_Async_VM_hard_shutdown(self, args: list) -> Any:
        """ Hard shut down a VM, returning a task uuid. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["power_state"] = "Halted"
        return _ok(self._make_task(status="success"))

    def _op_Async_VM_clean_reboot(self, args: list) -> Any:
        """ Reboot a VM, returning a task uuid. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["power_state"] = "Running"
        return _ok(self._make_task(status="success"))

    def _op_Async_VM_suspend(self, args: list) -> Any:
        """ Suspend a VM, returning a task uuid. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["power_state"] = "Suspended"
        return _ok(self._make_task(status="success"))

    def _op_Async_VM_resume(self, args: list) -> Any:
        """ Resume a VM, returning a task uuid. """
        self.vms[self._uuid_of(opaque_ref=args[0])]["power_state"] = "Running"
        return _ok(self._make_task(status="success"))

    def _op_VM_destroy(self, args: list) -> Any:
        """ Destroy a VM by ref. """
        uuid = self._uuid_of(opaque_ref=args[0])
        if uuid in self.vms:
            del self.vms[uuid]
            return _ok(None)
        return _fail("HANDLE_INVALID", "VM", args[0])

    def _op_VM_snapshot(self, args: list) -> Any:
        """ Snapshot a VM, returning the snapshot ref. """
        source_uuid = self._uuid_of(opaque_ref=args[0])
        uuid = self._alloc(prefix="snap")
        self.vms[uuid] = {
            "uuid": uuid, "name_label": args[1], "name_description": "",
            "power_state": "Halted", "VCPUs_max": 1, "memory_static_max": 0,
            "is_a_template": False, "is_control_domain": False,
            "is_a_snapshot": True,
            "snapshot_of": self._ref(uuid=source_uuid),
            "snapshot_time": "20260519T00:00:00Z",
            "other_config": {}, "tags": [],
        }
        return _ok(self._ref(uuid=uuid))

    def _op_VM_revert(self, args: list) -> Any:
        """ Revert to a snapshot. """
        return _ok(None)

    # -- VBD / VIF ops -------------------------------------------------

    def _op_VBD_create(self, args: list) -> Any:
        """ Create a VBD from a record dict. """
        record = args[0]
        uuid = self._alloc(prefix="vbd")
        self.vbds[uuid] = {
            "uuid": uuid, "VM": record["VM"], "VDI": record["VDI"],
            "userdevice": record["userdevice"],
            "bootable": record["bootable"],
        }
        return _ok(self._ref(uuid=uuid))

    def _op_VBD_get_uuid(self, args: list) -> Any:
        """ Return a VBD uuid for a ref. """
        return _ok(self._uuid_of(opaque_ref=args[0]))

    def _op_VBD_destroy(self, args: list) -> Any:
        """ Destroy a VBD by ref. """
        uuid = self._uuid_of(opaque_ref=args[0])
        if uuid in self.vbds:
            del self.vbds[uuid]
            return _ok(None)
        return _fail("HANDLE_INVALID", "VBD", args[0])

    def _op_VIF_create(self, args: list) -> Any:
        """ Create a VIF from a record dict. """
        record = args[0]
        uuid = self._alloc(prefix="vif")
        self.vifs[uuid] = {
            "uuid": uuid, "VM": record["VM"], "network": record["network"],
            "device": record["device"], "MAC": record.get("MAC", ""),
        }
        return _ok(self._ref(uuid=uuid))

    def _op_VIF_get_uuid(self, args: list) -> Any:
        """ Return a VIF uuid for a ref. """
        return _ok(self._uuid_of(opaque_ref=args[0]))

    def _op_VIF_destroy(self, args: list) -> Any:
        """ Destroy a VIF by ref. """
        uuid = self._uuid_of(opaque_ref=args[0])
        if uuid in self.vifs:
            del self.vifs[uuid]
            return _ok(None)
        return _fail("HANDLE_INVALID", "VIF", args[0])
