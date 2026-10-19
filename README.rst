==========================================
Code Craft AI Interop - XCP-ng / XenServer
==========================================

The ``codecraftai-interop-xen`` package is the venue-specific client for XCP-ng and Citrix
Hypervisor (XenServer) via the XAPI XML-RPC API exposed on the pool master. Although XAPI
rides over HTTPS, its serialization is XML-RPC — not REST — and its session model relies
on opaque per-call object references. For v1 this package uses direct XAPI bindings; the
"one transport per package" rule still applies.

Highlights
==========

- ``XenClient`` — the venue client speaking XAPI XML-RPC; session login/logout plus host and pool enumeration.
- Network and storage management — network and PIF/VIF management, storage repository (SR) and virtual disk image (VDI) management.
- VM lifecycle — template enumeration and VM provisioning from template, start/clean shutdown/hard shutdown/reboot/destroy, and VBD/VIF attach-detach.
- Snapshots and task handles — snapshot management and task tracking via XAPI's first-class ``task`` objects; the ref-based object model is hidden behind typed records on the way out.
- Aspects-driven transport — authentication uses ``XenSessionCredential`` (pool master URL + username + password); every behaviour-bearing call accepts ``aspects: AspectsXapi = DEFAULT_XEN_ASPECTS``.

Repository Structure
====================

- ``development/`` - Runtime environment scripts.
- ``repository-setup/`` - Repository homing and setup scripts.
- ``source/packages/ccai/interop/xen/`` - Package source code.
- ``source/testroots/testbase/ccai/tests/interop/xen/`` - TestBase test roots.
- ``specs/`` - Requirements, design, and task documentation (Kiro-style).
- ``userguide/`` - Standards, conventions, and documentation.

Environment Setup
=================

When working in a Codex container:

.. code-block:: bash

   ./development/setup-agent-container

For local development:

.. code-block:: bash

   ./repository-setup/rehome-repository
   ./development/setup-environment

Running Tests
=============

.. code-block:: bash

   source .venv/bin/activate
   testbase testing run --root ./source/testroots/testbase --includes=testbase.ccai.tests

Standards and Conventions
=========================

- Naming conventions: ``userguide/10-02-naming-conventions.rst``
- Code organization: ``userguide/10-01-code-organization.rst``
- Coding standards: ``userguide/10-00-coding-standards.rst``

Additional Resources
====================

- User guide entry point: ``userguide/userguide.rst``
