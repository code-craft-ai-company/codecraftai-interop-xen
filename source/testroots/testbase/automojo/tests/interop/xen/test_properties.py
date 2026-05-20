"""
    .. module:: test_properties
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Property-based tests for the XenTaskHandle waiter and the
        idempotent-retry semantics of the create/attach operations.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from hypothesis import given, settings, strategies as st

from automojo.interfaces.itaskhandle import TaskState

from automojo.interop.xen.aspectsxen import AspectsXapi
from automojo.interop.xen.model.xentaskhandle import XenTaskHandle
from automojo.interop.xen.model.xentaskstatus import (
    PENDING, SUCCESS, XenTaskStatus
)
from automojo.interop.xen.refs.refresolver import RefResolver
from automojo.interop.xen.session.xensessioncredential import (
    XenSessionCredential
)
from automojo.interop.xen.specs.xenvdispec import XenVdiSpec
from automojo.interop.xen.xenclient import XenClient

from ._mockxapi import MockXapiTransport


@given(pending_polls=st.integers(min_value=0, max_value=25),
       final_progress=st.floats(min_value=0.0, max_value=1.0))
def test_property_handle_wait_succeeds_after_any_pending_count(
        pending_polls, final_progress) -> None:
    """
        Regardless of how many PENDING polls precede it, the waiter returns
        a SUCCEEDED result once a terminal SUCCESS status is observed, and
        the reported progress is the fractional progress scaled to percent.
    """
    statuses = [XenTaskStatus(uuid="t", status=PENDING)
                for _ in range(pending_polls)]
    statuses.append(XenTaskStatus(uuid="t", status=SUCCESS,
                                  progress=final_progress))

    def fetch(uuid):
        return statuses.pop(0)

    handle = XenTaskHandle(task_uuid="t", status_fetcher=fetch,
                           sleeper=lambda s: None)
    result = handle.wait(aspects=AspectsXapi(completion_interval=0.0,
                                             completion_timeout=1e9))
    assert result.state == TaskState.SUCCEEDED
    assert result.progress == int(final_progress * 100)
    return


def _fresh_client():
    """
        Build a XenClient on a fresh mock transport with fast aspects.
    """
    transport = MockXapiTransport()
    credential = XenSessionCredential(master_url="https://xen.lab",
                                      username="root", password="secret")
    aspects = AspectsXapi(completion_interval=0.0, completion_timeout=5.0)
    client = XenClient(credential=credential,
                       transport_factory=lambda *, master_url: transport,
                       aspects=aspects)
    rtnval = (client, aspects)
    return rtnval


@given(repeat_count=st.integers(min_value=1, max_value=6),
       size=st.integers(min_value=1024, max_value=1099511627776))
@settings(deadline=None)
def test_property_vdi_create_is_idempotent_under_repetition(
        repeat_count, size) -> None:
    """
        Creating the same VDI spec any number of times yields exactly one
        VDI whose uuid is stable across every repeated create.
    """
    client, aspects = _fresh_client()
    client.Sr.list(aspects=aspects)
    spec = XenVdiSpec(name_label="prop-disk", sr_uuid="sr-uuid-1",
                      virtual_size=size)

    seen_uuids = set()
    for _ in range(repeat_count):
        vdi = client.Vdi.create(spec=spec, aspects=aspects)
        seen_uuids.add(vdi.uuid)

    assert len(seen_uuids) == 1
    assert len(client.Vdi.list(aspects=aspects)) == 1
    return


@given(invalid_call_index=st.integers(min_value=1, max_value=3))
@settings(deadline=None)
def test_property_relogin_preserves_enumeration_result(
        invalid_call_index) -> None:
    """
        A SESSION_INVALID fault injected on any early call is recovered by
        transparent re-login; the enumeration result is unchanged.
    """
    transport = MockXapiTransport()
    transport.session_invalid_on_call = invalid_call_index
    credential = XenSessionCredential(master_url="https://xen.lab",
                                      username="root", password="secret")
    aspects = AspectsXapi(completion_interval=0.0, max_attempts=3)
    client = XenClient(credential=credential,
                       transport_factory=lambda *, master_url: transport,
                       aspects=aspects)
    hosts = client.Hosts.list(aspects=aspects)
    assert len(hosts) == 1
    return


@given(uuid=st.text(min_size=1, max_size=12))
def test_property_record_ref_remembers_uuid_pairs(uuid) -> None:
    """
        A record carrying a uuid is recorded by the resolver so the opaque
        ref then translates back to that uuid.
    """
    from automojo.interop.xen.apigroups.basegroup import BaseGroup

    resolver = RefResolver()
    group = BaseGroup(session_manager=None, resolver=resolver)
    opaque_ref = "OpaqueRef:{}".format(uuid)
    group._record_ref(opaque_ref=opaque_ref, record={"uuid": uuid})
    assert resolver.uuid_for(opaque_ref=opaque_ref) == uuid
    return
