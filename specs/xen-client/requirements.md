# Requirements

## Introduction

The `xen-client` feature provides a typed Python client for XCP-ng /
XenServer's XAPI XML-RPC API on the pool master. Because XAPI is
XML-RPC and not REST, this client does **not** use `RestClientBase` for
v1. The "one transport per package" rule still applies.

The client covers session lifecycle, host/pool/network enumeration,
storage repository and VDI management, template enumeration and VM
provisioning, VM lifecycle, VBD/VIF attach-detach, snapshot management,
and XAPI task tracking. Every behaviour-bearing method accepts
`aspects: AspectsXapi = DEFAULT_XEN_ASPECTS`.

---

## Requirements

### Requirement 1: Session Login and Logout

#### Acceptance Criteria

1. WHEN the client is constructed with a `XenSessionCredential` THE
   SYSTEM SHALL call `session.login_with_password` on first use and
   cache the session id.
2. WHEN the pool master URL or credentials are missing THE SYSTEM SHALL
   raise `ConfigurationError`.
3. WHEN a call returns `SESSION_INVALID` THE SYSTEM SHALL re-login
   transparently and retry the original call.
4. WHEN the caller invokes `logout(aspects)` THE SYSTEM SHALL release
   the session.
5. WHEN login fails with an authentication error THE SYSTEM SHALL raise
   `XenAuthenticationError`.

### Requirement 2: Enumerate Hosts, Pool, and Networks

#### Acceptance Criteria

1. WHEN the caller invokes `list_hosts(aspects)` THE SYSTEM SHALL
   return `XenHost` records (uuid, name_label, address, enabled).
2. WHEN the caller invokes `get_pool(aspects)` THE SYSTEM SHALL return
   a `XenPool` record.
3. WHEN the caller invokes `list_networks(aspects)` and
   `list_pifs(host_uuid, aspects)` THE SYSTEM SHALL return typed
   records resolving XAPI opaque refs to uuids.

### Requirement 3: Manage Storage Repositories and VDIs

#### Acceptance Criteria

1. WHEN the caller invokes `list_storage_repositories(aspects)` THE
   SYSTEM SHALL return `XenStorageRepository` records (uuid, type,
   capacity, free).
2. WHEN the caller invokes `create_vdi(spec, aspects)`,
   `list_vdis(sr_uuid, aspects)`, `delete_vdi(vdi_uuid, aspects)`, or
   `resize_vdi(vdi_uuid, size_bytes, aspects)` THE SYSTEM SHALL perform
   the corresponding XAPI call with idempotent delete.

### Requirement 4: Enumerate Templates

#### Acceptance Criteria

1. WHEN the caller invokes `list_templates(aspects)` THE SYSTEM SHALL
   return `XenVmTemplate` records (uuid, name_label, name_description,
   os_version_hint).

### Requirement 5: Provision a VM from a Template

#### Acceptance Criteria

1. WHEN the caller invokes `clone_vm_from_template(template_uuid, spec, aspects)`
   THE SYSTEM SHALL call `VM.clone`, apply the spec's overrides
   (memory, vCPUs, name_label, name_description, other_config),
   `VM.provision`, and return both a `XenVm` record and a
   `XenTaskHandle` covering the chained operation.
2. WHEN a VM with the same `name_label` already exists THE SYSTEM SHALL
   return the existing record (read-before-create).

### Requirement 6: Manage VM Lifecycle

#### Acceptance Criteria

1. WHEN the caller invokes `start_vm`, `clean_shutdown_vm`,
   `hard_shutdown_vm`, `reboot_vm`, `suspend_vm`, `resume_vm`, or
   `destroy_vm` THE SYSTEM SHALL call the corresponding XAPI op and
   return a `XenTaskHandle` for async ops.
2. WHEN `destroy_vm` targets an unknown uuid THE SYSTEM SHALL succeed
   as a no-op.
3. WHEN the caller invokes `get_vm(vm_uuid, aspects)` and
   `list_vms(aspects)` THE SYSTEM SHALL return typed records (no opaque
   refs in the public shape).

### Requirement 7: Manage VBDs and VIFs

#### Acceptance Criteria

1. WHEN the caller invokes `attach_vbd(vm_uuid, vdi_uuid, userdevice, aspects)`,
   `detach_vbd(vbd_uuid, aspects)`,
   `attach_vif(vm_uuid, network_uuid, device, aspects)`, or
   `detach_vif(vif_uuid, aspects)` THE SYSTEM SHALL perform the XAPI op.
2. Idempotent attach when an identical VBD/VIF already exists; idempotent
   detach when the device is already absent.

### Requirement 8: Manage Snapshots

#### Acceptance Criteria

1. WHEN the caller invokes `snapshot_vm(vm_uuid, name, aspects)`,
   `list_vm_snapshots(vm_uuid, aspects)`,
   `revert_vm_snapshot(snapshot_uuid, aspects)`, or
   `destroy_vm_snapshot(snapshot_uuid, aspects)` THE SYSTEM SHALL
   perform the XAPI op with idempotent destroy.

### Requirement 9: Track XAPI Tasks

#### Acceptance Criteria

1. WHEN any async op returns a `task` ref THE SYSTEM SHALL return a
   `XenTaskHandle` implementing `ITaskHandle`.
2. WHEN `handle.wait(aspects)` is invoked THE SYSTEM SHALL poll the
   task's status field per aspects.
3. WHEN the aspects timeout elapses THE SYSTEM SHALL raise
   `TimeoutError`.
4. WHEN the task ends in `failure` THE SYSTEM SHALL raise
   `XenTaskFailedError` with the error_info payload.

### Requirement 10: Wait For VM Power State

#### Acceptance Criteria

1. WHEN the caller invokes `wait_for_power_state(vm_uuid, desired_state, aspects)`
   THE SYSTEM SHALL poll per aspects and SHALL raise `TimeoutError` on
   budget exhaustion.

### Requirement 11: Aspects on Every Behaviour-Bearing Call

#### Acceptance Criteria

1. THE SYSTEM SHALL accept `aspects: AspectsXapi = DEFAULT_XEN_ASPECTS`
   on every I/O method; no behaviour-modifying decorators.
