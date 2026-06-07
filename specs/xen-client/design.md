# Design

## Overview

`XenClient` is a typed Python client for XAPI XML-RPC on XCP-ng /
XenServer. The XAPI object model returns opaque refs; the client
resolves them to typed records keyed by uuid before exposing them to
callers. Async ops return a typed `XenTaskHandle`.

This client does NOT use `RestClientBase`. A future REST/XML-RPC variant
of the base could be explored, but for v1 the transport is XAPI-native.
"One transport per package" still holds.

---

## Architecture

```
┌────────────────────────────────────────────────────────┐
│  codecraftai-provisioning / venues / xcpng                │
└──────────┬─────────────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────────────────────┐
│  XenClient (this package)                              │
│   XAPI XML-RPC bindings                                │
│   AspectsXapi on every op                              │
│   Opaque-ref → typed-record resolution                 │
│   API groups: session, pool, hosts, networks,          │
│     storage-repositories, vdis, templates, vms,        │
│     vbds, vifs, snapshots, tasks                       │
└──────────┬─────────────────────────────────────────────┘
           │ HTTPS XML-RPC to pool master
           ▼
┌────────────────────────────────────────────────────────┐
│  XCP-ng / XenServer pool master                        │
└────────────────────────────────────────────────────────┘
```

---

## Data Model

`model/`: `xenpool.py`, `xenhost.py`, `xennetwork.py`, `xenpif.py`,
`xenstoragerepository.py`, `xenvdi.py`, `xenvmtemplate.py`, `xenvm.py`,
`xenvbd.py`, `xenvif.py`, `xenvmsnapshot.py`, `xentaskstatus.py`,
`xentaskhandle.py`.

`specs/`: `xenvdispec.py`, `xenvmclonespec.py`, `xenvbdspec.py`,
`xenvifspec.py`.

Exceptions: `XenAuthenticationError`, `XenTaskFailedError`.

---

## Module Layout

```
source/packages/ccai/interop/xen/
├── xenclient.py
├── aspectsxen.py
├── session/
│   └── xensessionmanager.py
├── apigroups/{poolgroup, hostsgroup, networksgroup, srgroup, vdigroup,
│              templatesgroup, vmsgroup, vbdsgroup, vifsgroup,
│              snapshotsgroup, tasksgroup}.py
├── refs/
│   └── refresolver.py            # opaque-ref ↔ uuid round-trip
├── model/
├── specs/
└── exceptions/
```

---

## See Also

- `codecraftai-provisioning/specs/venue-xcpng/`
- Cross-cutting usability commitment §8.1 — XAPI is the second native-shape example after libvirt.

---

## Testing Strategy

Example-based tests cover session login, transparent re-login on
`SESSION_INVALID`, idempotent VDI/VM/snapshot operations, template
clone-and-provision flow, and XAPI task completion using a mock XAPI
transport.

Property-based tests (hypothesis) are **required** for:
1. **Opaque-ref ↔ typed-record round-tripping.** For any pair of
   (record, opaque-ref) in the mock transport, resolving in either
   direction is total and consistent.
2. **Idempotent retry semantics** within and beyond the aspects budget.
3. **`XenTaskHandle.wait`** terminal-state correctness over arbitrary
   monotonic mock status streams.
4. **Transparent re-login.** For any sequence of calls that intersperses
   `SESSION_INVALID` failures, the observable behaviour equals the
   single-login success case.
