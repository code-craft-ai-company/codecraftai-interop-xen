"""
    .. module:: xentaskstatus
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed snapshot of an XAPI task object's status.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass
from typing import Any, Optional


# XAPI task ``status`` field values.  ``pending`` is non-terminal; the
# remaining values are terminal.
PENDING = "pending"
SUCCESS = "success"
FAILURE = "failure"
CANCELLING = "cancelling"
CANCELLED = "cancelled"

TERMINAL_STATUSES = frozenset({SUCCESS, FAILURE, CANCELLED})


@dataclass
class XenTaskStatus:
    """
        Snapshot of an XAPI task's status at one observation point.

        :param uuid: The task uuid.
        :param status: One of ``pending``, ``success``, ``failure``,
                       ``cancelling`` or ``cancelled``.
        :param progress: Fractional progress in the range 0.0 to 1.0.
        :param result: The task result reference string, when present.
        :param error_info: The XAPI ``error_info`` payload on failure.
    """
    uuid: str
    status: str = PENDING
    progress: float = 0.0
    result: Optional[str] = None
    error_info: Optional[Any] = None

    @property
    def is_terminal(self) -> bool:
        """
            Report whether the task has reached a terminal status.

            :returns: True when the status is success, failure or cancelled.
        """
        rtnval = self.status in TERMINAL_STATUSES
        return rtnval
