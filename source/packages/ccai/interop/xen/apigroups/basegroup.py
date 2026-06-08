"""
    .. module:: basegroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: BaseGroup — common base for the XAPI client API groups,
        carrying the session manager and ref resolver.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import Any, List

from ccai.interop.xen.aspectsxen import AspectsXapi
from ccai.interop.xen.refs.refresolver import RefResolver
from ccai.interop.xen.session.xensessionmanager import XenSessionManager


class BaseGroup:
    """
        Common base for XAPI client API groups.

        Holds the shared :class:`XenSessionManager` (which owns the XML-RPC
        transport) and the shared :class:`RefResolver` (opaque-ref/uuid
        translation cache).  Subclasses dispatch XAPI calls through
        :meth:`_call` and resolve refs through the resolver.
    """

    def __init__(self, *, session_manager: XenSessionManager,
                 resolver: RefResolver) -> None:
        """
            Construct a BaseGroup.

            :param session_manager: The shared XenSessionManager.
            :param resolver: The shared RefResolver.
        """
        self._session_manager: XenSessionManager = session_manager
        self._resolver: RefResolver = resolver
        return

    def _call(self, *, method_path: str, args: List[Any],
              aspects: AspectsXapi) -> Any:
        """
            Dispatch an XAPI XML-RPC call through the session manager.

            :param method_path: Dotted XAPI method path.
            :param args: Positional XAPI arguments after the session ref.
            :param aspects: Behaviour controls.

            :returns: The unwrapped XAPI ``Value`` payload.
        """
        rtnval = self._session_manager.dispatch(
            method_path=method_path, args=args, aspects=aspects)
        return rtnval

    def _record_ref(self, *, opaque_ref: str, record: Any) -> None:
        """
            Record the opaque-ref/uuid pairing for a fetched XAPI record.

            :param opaque_ref: The XAPI opaque reference.
            :param record: The XAPI record dict carrying a ``uuid`` field.
        """
        if isinstance(record, dict):
            uuid = record.get("uuid", None)
            if uuid is not None:
                self._resolver.remember(opaque_ref=opaque_ref, uuid=uuid)
        return
