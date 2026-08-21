"""
    .. module:: test_tasks
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Task status and XenTaskHandle poll-loop tests.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from ccai import testbase


from ccai.interfaces.itaskhandle import ITaskHandle, TaskState

from ccai.interop.xen.aspectsxen import AspectsXapi
from ccai.interop.xen.exceptions.xenexceptions import XenTaskFailedError
from ccai.interop.xen.model.xentaskhandle import XenTaskHandle
from ccai.interop.xen.model.xentaskstatus import (
    CANCELLED, FAILURE, PENDING, SUCCESS, XenTaskStatus
)

from .factories import (create_xen_client, create_xen_transport)


@testbase.attach.parameter(create_xen_client, identifier="client")
@testbase.attach.parameter(create_xen_transport, identifier="transport")
def test_tasks_get_status_returns_typed_snapshot(transport,
                                                 client,
                                                 fast_aspects) -> None:
    """
        Tasks.get_status returns a typed XenTaskStatus for a task uuid.
    """
    task_uuid = transport._make_task(status="success", result="OpaqueRef:x")
    status = client.Tasks.get_status(task_uuid=task_uuid,
                                     aspects=fast_aspects)
    assert isinstance(status, XenTaskStatus)
    assert status.status == SUCCESS
    assert status.is_terminal is True
    return


def test_xentaskhandle_conforms_to_itaskhandle() -> None:
    """
        XenTaskHandle is recognised structurally as an ITaskHandle.
    """
    handle = XenTaskHandle(task_uuid="task-1",
                           status_fetcher=lambda u: XenTaskStatus(uuid=u))
    assert isinstance(handle, ITaskHandle)
    return


def test_task_status_terminal_classification() -> None:
    """
        XenTaskStatus.is_terminal is true only for terminal statuses.
    """
    assert XenTaskStatus(uuid="t", status=PENDING).is_terminal is False
    assert XenTaskStatus(uuid="t", status=SUCCESS).is_terminal is True
    assert XenTaskStatus(uuid="t", status=FAILURE).is_terminal is True
    assert XenTaskStatus(uuid="t", status=CANCELLED).is_terminal is True
    return


def test_handle_wait_success() -> None:
    """
        wait returns a SUCCEEDED TaskResult for a successful task.
    """
    statuses = [
        XenTaskStatus(uuid="t", status=PENDING, progress=0.5),
        XenTaskStatus(uuid="t", status=SUCCESS, progress=1.0,
                      result="OpaqueRef:done"),
    ]

    def fetch(uuid):
        return statuses.pop(0)

    handle = XenTaskHandle(task_uuid="t", status_fetcher=fetch,
                           sleeper=lambda s: None)
    result = handle.wait(aspects=AspectsXapi(completion_interval=0.0))
    assert result.state == TaskState.SUCCEEDED
    assert result.progress == 100
    assert handle.is_done() is True
    return


def test_handle_wait_failure_raises() -> None:
    """
        wait raises XenTaskFailedError carrying error_info on failure.
    """
    def fetch(uuid):
        return XenTaskStatus(uuid="t", status=FAILURE,
                             error_info=["INTERNAL_ERROR", "boom"])

    handle = XenTaskHandle(task_uuid="t", status_fetcher=fetch,
                           sleeper=lambda s: None)
    with testbase.raises(XenTaskFailedError) as caught:
        handle.wait(aspects=AspectsXapi(completion_interval=0.0))
    assert caught.value.error_info == ["INTERNAL_ERROR", "boom"]
    return


def test_handle_wait_cancelled() -> None:
    """
        wait returns a CANCELLED TaskResult for a cancelled task.
    """
    def fetch(uuid):
        return XenTaskStatus(uuid="t", status=CANCELLED)

    handle = XenTaskHandle(task_uuid="t", status_fetcher=fetch,
                           sleeper=lambda s: None)
    result = handle.wait(aspects=AspectsXapi(completion_interval=0.0))
    assert result.state == TaskState.CANCELLED
    return


def test_handle_wait_times_out() -> None:
    """
        wait raises TimeoutError when the task never reaches a terminal
        status before the completion timeout.
    """
    ticks = [0.0, 0.0, 100.0, 200.0]

    def clock():
        return ticks.pop(0) if len(ticks) > 1 else ticks[0]

    def fetch(uuid):
        return XenTaskStatus(uuid="t", status=PENDING)

    handle = XenTaskHandle(task_uuid="t", status_fetcher=fetch,
                           sleeper=lambda s: None, clock=clock)
    aspects = AspectsXapi(completion_interval=0.0, completion_timeout=10.0)
    with testbase.raises(TimeoutError):
        handle.wait(aspects=aspects)
    return


def test_handle_cancel_without_canceller_raises() -> None:
    """
        cancel raises NotImplementedError when no canceller was supplied.
    """
    handle = XenTaskHandle(task_uuid="t",
                           status_fetcher=lambda u: XenTaskStatus(uuid=u))
    with testbase.raises(NotImplementedError):
        handle.cancel()
    return


def test_handle_cancel_invokes_canceller() -> None:
    """
        cancel invokes the supplied canceller for a non-terminal task.
    """
    cancelled = []
    handle = XenTaskHandle(task_uuid="t",
                           status_fetcher=lambda u: XenTaskStatus(uuid=u),
                           canceller=lambda u: cancelled.append(u))
    handle.cancel()
    assert cancelled == ["t"]
    return


def test_handle_cancel_terminal_is_noop() -> None:
    """
        cancel is a no-op once the task has reached a terminal status.
    """
    handle = XenTaskHandle(
        task_uuid="t",
        status_fetcher=lambda u: XenTaskStatus(uuid=u, status=SUCCESS),
        sleeper=lambda s: None)
    handle.status()
    handle.cancel()
    return
