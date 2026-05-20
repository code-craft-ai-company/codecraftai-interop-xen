# Implementation Plan — Xen Client

## Package Skeleton

- [x] 1. Create `source/packages/automojo/interop/xen/` package tree with `session/`, `apigroups/`, `refs/`, `model/`, `specs/`, `exceptions/` subpackages.
- [x] 2. Add `aspectsxen.py` defining `AspectsXapi` and `DEFAULT_XEN_ASPECTS`.

## Session Lifecycle

- [x] 3. Implement `XenSessionManager` (login, transparent re-login on `SESSION_INVALID`, logout).
- [x] 4. Implement `RefResolver` (opaque ref ↔ uuid translation cache).

## API Groups

- [x] 5. Implement `PoolGroup.get`, `HostsGroup.list`, `NetworksGroup.list`, `PifsGroup.list`.
- [x] 6. Implement `SrGroup.list` and `VdiGroup.create / list / delete / resize` with idempotent delete.
- [x] 7. Implement `TemplatesGroup.list`.
- [x] 8. Implement `VmsGroup.clone_from_template / get / list / start / clean_shutdown / hard_shutdown / reboot / suspend / resume / destroy` with idempotent destroy and read-before-create on clone.
- [x] 9. Implement `VbdsGroup.attach / detach` and `VifsGroup.attach / detach` with idempotency.
- [x] 10. Implement `SnapshotsGroup.snapshot_vm / list / revert / destroy` with idempotent destroy.
- [x] 11. Implement `TasksGroup.get_status` consumed by `XenTaskHandle.wait`.

## Data Model & Specs

- [x] 12. Implement model dataclasses for all enumerated entities.
- [x] 13. Implement spec dataclasses for VDI/VM-clone/VBD/VIF.
- [x] 14. Implement `XenTaskHandle` against `ITaskHandle`.

## Waiters

- [x] 15. Implement `wait_for_power_state(vm_uuid, desired_state, aspects)`.

## Tests — Example-Based

- [x] 16. Session login + transparent re-login tests using a mock XAPI module.
- [x] 17. Idempotent VDI/VM/snapshot create/destroy tests.
- [x] 18. Template clone-and-provision flow.
- [x] 19. XAPI task completion + failure-reclassification tests.

## Tests — Property-Based (hypothesis)

- [x] 20. Opaque-ref ↔ uuid round-trip totality and consistency.
- [x] 21. Idempotent-retry equivalence.
- [x] 22. `XenTaskHandle.wait` terminal-state correctness.
- [x] 23. Transparent re-login equivalence across arbitrary `SESSION_INVALID` interleavings.

## Integration

- [ ] 24. Smoke-test fixture against a live XCP-ng pool master, gated by env var.
