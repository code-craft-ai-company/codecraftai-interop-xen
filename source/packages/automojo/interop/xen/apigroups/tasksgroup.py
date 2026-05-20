"""
    .. module:: tasksgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: TasksGroup — XAPI task status enumeration consumed by
        :class:`XenTaskHandle`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from automojo.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from automojo.interop.xen.apigroups.basegroup import BaseGroup
from automojo.interop.xen.model.xentaskstatus import PENDING, XenTaskStatus


class TasksGroup(BaseGroup):
    """
        XAPI ``task`` object-class operations.
    """

    def get_status(self, *, task_uuid: str,
                   aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                   ) -> XenTaskStatus:
        """
            Fetch the current status of an XAPI task.

            :param task_uuid: The task uuid.
            :param aspects: Behaviour controls.

            :returns: A :class:`XenTaskStatus` snapshot.
        """
        task_ref = self._call(method_path="task.get_by_uuid",
                              args=[task_uuid], aspects=aspects)
        record = self._call(method_path="task.get_record", args=[task_ref],
                             aspects=aspects)

        status = PENDING
        progress = 0.0
        result = None
        error_info = None
        if isinstance(record, dict):
            status = record.get("status", PENDING)
            progress = float(record.get("progress", 0.0))
            result = record.get("result", None)
            error_info = record.get("error_info", None)

        rtnval = XenTaskStatus(
            uuid=task_uuid, status=status, progress=progress,
            result=result, error_info=error_info,
        )
        return rtnval
