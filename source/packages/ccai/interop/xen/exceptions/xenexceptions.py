"""
    .. module:: xenexceptions
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Exception types raised by the XAPI XML-RPC client.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import Any, Optional


# XAPI fault code returned when an operation targets an opaque ref / handle that
# no longer exists (the object is already absent).
HANDLE_INVALID = "HANDLE_INVALID"


def is_handle_invalid(xcpt: Exception) -> bool:
    """
        Reports whether an exception is an XAPI ``HANDLE_INVALID`` fault, i.e. the
        target object is already absent.

        Idempotent destroy/detach/delete operations may treat this as a no-op, but
        must NOT swallow other ``XenError`` faults (device-in-use,
        OPERATION_NOT_ALLOWED, permission, ...) which represent genuine failures.

        :param xcpt: The exception to classify.

        :returns: ``True`` when the fault indicates an already-absent handle.
    """
    rtnval = HANDLE_INVALID in str(xcpt)
    return rtnval


class XenError(RuntimeError):
    """
        Base error for every failure surfaced by the XAPI client.
    """


class XenAuthenticationError(XenError):
    """
        Raised when ``session.login_with_password`` fails because the
        supplied credential was rejected by the pool master.
    """


class XenTaskFailedError(XenError):
    """
        Raised when an XAPI ``task`` object ends in the ``failure`` status.

        The originating ``error_info`` payload is preserved on the instance so
        callers can inspect the XAPI fault detail.
    """

    def __init__(self, message: str,
                 error_info: Optional[Any] = None) -> None:
        """
            Initialise with a message and the failing task's error_info.

            :param message: Multi-line error text.
            :param error_info: The XAPI task ``error_info`` payload.
        """
        super().__init__(message)
        self.error_info: Optional[Any] = error_info
        return


__all__ = ["XenError", "XenAuthenticationError", "XenTaskFailedError", "HANDLE_INVALID", "is_handle_invalid"]
