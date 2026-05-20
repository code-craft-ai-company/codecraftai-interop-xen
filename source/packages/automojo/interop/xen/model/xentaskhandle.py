"""
    .. module:: xentaskhandle
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Provides :class:`XenTaskHandle`, the synchronous,
        Aspects-driven poll handle returned by every async XAPI operation.
        Conforms structurally to :class:`ITaskHandle`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import logging
import os
import time

from typing import Callable, Optional

from automojo.interfaces.itaskhandle import (
    ITaskHandle, TaskResult, TaskState
)

from automojo.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from automojo.interop.xen.exceptions.xenexceptions import XenTaskFailedError
from automojo.interop.xen.model.xentaskstatus import (
    CANCELLED, FAILURE, SUCCESS, XenTaskStatus
)


_IFACE_STATE_MAP = {
    SUCCESS: TaskState.SUCCEEDED,
    FAILURE: TaskState.FAILED,
    CANCELLED: TaskState.CANCELLED,
}


class XenTaskHandle:
    """
        Synchronous, Aspects-driven handle on an XAPI ``task`` object.

        The handle conforms structurally to
        :class:`automojo.interfaces.itaskhandle.ITaskHandle` so it is
        recognised by ``isinstance(handle, ITaskHandle)``.  The poll loop is
        driven by :class:`AspectsXapi`; the elapsed-time gate is evaluated at
        the top of every iteration so a slow status fetch cannot blow past
        the completion timeout.
    """

    def __init__(self, *, task_uuid: str,
                 status_fetcher: Callable[[str], XenTaskStatus],
                 canceller: Optional[Callable[[str], None]] = None,
                 sleeper: Optional[Callable[[float], None]] = None,
                 clock: Optional[Callable[[], float]] = None) -> None:
        """
            Initialise an XAPI task handle.

            :param task_uuid: The XAPI-assigned task uuid.
            :param status_fetcher: Callable returning a fresh
                                   :class:`XenTaskStatus` for the task uuid.
            :param canceller: Optional callable that requests cancellation.
            :param sleeper: Optional override for ``time.sleep`` (tests).
            :param clock: Optional override for ``time.monotonic`` (tests).
        """
        self._task_uuid: str = task_uuid
        self._status_fetcher: Callable[[str], XenTaskStatus] = status_fetcher
        self._canceller: Optional[Callable[[str], None]] = canceller
        self._sleeper: Optional[Callable[[float], None]] = sleeper
        self._clock: Optional[Callable[[], float]] = clock
        self._last_status: Optional[XenTaskStatus] = None
        return

    def task_id(self) -> str:
        """
            Return the XAPI task uuid.

            :returns: The task uuid string.
        """
        rtnval = self._task_uuid
        return rtnval

    def is_done(self) -> bool:
        """
            Report whether the last observed status was terminal.

            :returns: True when the last observed status was terminal.
        """
        if self._last_status is None:
            rtnval = False
            return rtnval
        rtnval = self._last_status.is_terminal
        return rtnval

    def status(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
               ) -> XenTaskStatus:
        """
            Fetch and cache the current task status.

            :param aspects: Behaviour controls (carried for symmetry).

            :returns: A freshly observed :class:`XenTaskStatus`.
        """
        _ = aspects
        observed = self._status_fetcher(self._task_uuid)
        self._last_status = observed
        rtnval = observed
        return rtnval

    def wait(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
             ) -> TaskResult:
        """
            Poll the XAPI task until it reaches a terminal status.

            :param aspects: Behaviour controls; ``completion_interval`` is the
                            poll interval and ``completion_timeout`` the
                            wall-clock cap.

            :returns: A :class:`TaskResult` describing the terminal state.
            :raises: TimeoutError, XenTaskFailedError
        """
        interval = aspects.completion_interval
        timeout = aspects.completion_timeout

        clock = self._clock if self._clock is not None else time.monotonic
        sleeper = self._sleeper if self._sleeper is not None else time.sleep

        logger_name = aspects.logger_name
        if logger_name is None:
            logger_name = "automojo.interop.xen"
        logger = logging.getLogger(logger_name)

        started = clock()
        last_status_value: Optional[str] = None
        rtnval: Optional[TaskResult] = None

        while True:
            elapsed = clock() - started
            if elapsed > timeout:
                err_msg_lines = ["XenTaskHandle.wait timed out."]
                err_msg_lines.append("TASK: {}".format(self._task_uuid))
                err_msg_lines.append("TIMEOUT: {}s".format(timeout))
                err_msg_lines.append("ELAPSED: {}s".format(elapsed))
                last_value = (last_status_value if last_status_value
                              is not None else "<none>")
                err_msg_lines.append("LAST STATUS: {}".format(last_value))
                err_msg = os.linesep.join(err_msg_lines)
                raise TimeoutError(err_msg)

            observed = self.status(aspects=aspects)

            if observed.status != last_status_value:
                logger.info("task %s status: %s", self._task_uuid,
                            observed.status)
                last_status_value = observed.status

            if observed.is_terminal is True:
                if observed.status == SUCCESS:
                    rtnval = TaskResult(
                        task_id=self._task_uuid,
                        state=TaskState.SUCCEEDED,
                        progress=int(observed.progress * 100),
                        error=None,
                        payload={"result": observed.result},
                    )
                    break
                if observed.status == CANCELLED:
                    rtnval = TaskResult(
                        task_id=self._task_uuid,
                        state=TaskState.CANCELLED,
                        progress=int(observed.progress * 100),
                        error=None, payload=None,
                    )
                    break

                err_msg_lines = ["XAPI task reached the failure status."]
                err_msg_lines.append("TASK: {}".format(self._task_uuid))
                err_msg_lines.append("ERROR_INFO: {!r}".format(
                    observed.error_info))
                err_msg = os.linesep.join(err_msg_lines)
                raise XenTaskFailedError(err_msg,
                                         error_info=observed.error_info)

            sleeper(interval)

        return rtnval

    def cancel(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Request cancellation of the in-flight XAPI task.

            When the task is already terminal this is a no-op.

            :param aspects: Behaviour controls.

            :raises: NotImplementedError
        """
        _ = aspects
        if self._last_status is not None and self._last_status.is_terminal:
            return

        if self._canceller is None:
            err_msg = ("XenTaskHandle.cancel: no canceller was supplied for "
                       "task {}.".format(self._task_uuid))
            raise NotImplementedError(err_msg)

        self._canceller(self._task_uuid)
        return


# Runtime conformance attestation.  ``ITaskHandle`` is a runtime-checkable
# Protocol; this binding makes the structural relationship explicit.
_ITASKHANDLE_PROTOCOL = ITaskHandle
