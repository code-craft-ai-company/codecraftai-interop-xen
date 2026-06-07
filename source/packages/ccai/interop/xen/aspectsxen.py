"""
    .. module:: aspectsxen
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Provides the :class:`AspectsXapi` subclass and the
        ``DEFAULT_XEN_ASPECTS`` instance used by every behaviour-bearing
        method on :class:`XenClient` and its API groups.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import Optional

from ccai.aspects.aspects import Aspects


class AspectsXapi(Aspects):
    """
        XAPI-specialised :class:`Aspects` carrier.

        Packages the behaviour-modifying parameters every XAPI XML-RPC call
        accepts (poll interval, completion timeout, attempt budget, logging
        hint) into a single scalable parameter.  The class exists so callers
        can write ``aspects: AspectsXapi`` for clarity at call sites and so
        future XAPI-specific behaviour can be added without churning the
        public type signature on every group method.
    """

    def __init__(self, *,
                 completion_interval: float = 2.0,
                 completion_timeout: float = 600.0,
                 connection_timeout: float = 60.0,
                 max_attempts: int = 3,
                 logger_name: Optional[str] = None) -> None:
        """
            Initialise an XAPI-flavoured aspects bundle.

            :param completion_interval: Seconds between poll iterations.
            :param completion_timeout: Maximum seconds to wait for a task or
                                       power-state transition to complete.
            :param connection_timeout: Maximum seconds for a single XML-RPC
                                       attempt before reclassifying.
            :param max_attempts: Maximum attempts for transparent re-login and
                                 idempotent-retry semantics.
            :param logger_name: Optional logger name for routing log lines.
        """
        super().__init__(completion_interval=completion_interval,
                         completion_timeout=completion_timeout,
                         connection_timeout=connection_timeout,
                         max_attempts=max_attempts,
                         logger_name=logger_name)
        return


DEFAULT_XEN_ASPECTS = AspectsXapi()


__all__ = ["AspectsXapi", "DEFAULT_XEN_ASPECTS"]
