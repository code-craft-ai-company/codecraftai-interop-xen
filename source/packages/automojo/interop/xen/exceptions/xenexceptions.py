"""
    .. module:: xenexceptions
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Exception types raised by the XAPI XML-RPC client.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from typing import Any, Optional


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


__all__ = ["XenError", "XenAuthenticationError", "XenTaskFailedError"]
