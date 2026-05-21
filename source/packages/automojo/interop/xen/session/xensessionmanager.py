"""
    .. module:: xensessionmanager
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: XenSessionManager — owns the XAPI XML-RPC transport, the
        session login/logout lifecycle, and transparent re-login on
        ``SESSION_INVALID``.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import os

from typing import Any, Callable, List, Optional

from automojo.errors.exceptions import ConfigurationError, SemanticError

from automojo.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from automojo.interop.xen.exceptions.xenexceptions import (
    XenAuthenticationError, XenError
)
from automojo.interop.xen.session.xensessioncredential import (
    XenSessionCredential
)


# XAPI fault detail markers.  XAPI surfaces application-level faults inside
# the XML-RPC response envelope: ``{"Status": "Failure",
# "ErrorDescription": ["SESSION_INVALID", ...]}``.
SESSION_INVALID = "SESSION_INVALID"
_AUTH_FAILURE_CODES = frozenset({
    "SESSION_AUTHENTICATION_FAILED",
    "HOST_IS_SLAVE",
})


def _default_transport_factory(*, master_url: str) -> Any:
    """
        Build the default XAPI XML-RPC transport.

        The single-file ``XenAPI`` module is preferred when importable; it
        provides a session-aware proxy.  When it is unavailable the standard
        library ``xmlrpc.client.ServerProxy`` against the ``/RPC2`` endpoint
        is used instead — XAPI speaks XML-RPC, not REST, so this is a faithful
        fallback.  Both imports are deferred so unit tests that inject a mock
        transport never touch a real host.

        :param master_url: The pool-master URL.

        :returns: An object exposing dotted XAPI methods callable with the
                  XML-RPC convention.
    """
    try:
        import XenAPI  # noqa: F401  (single-file vendored module)
        rtnval = XenAPI.Session(master_url)
        return rtnval
    except ImportError:
        import xmlrpc.client
        endpoint = master_url
        if not endpoint.endswith("/RPC2"):
            endpoint = endpoint.rstrip("/") + "/RPC2"
        rtnval = xmlrpc.client.ServerProxy(endpoint, allow_none=True)
        return rtnval


class XenSessionManager:
    """
        Owns the XAPI XML-RPC transport and the session lifecycle.

        On first use the manager calls ``session.login_with_password`` and
        caches the returned session reference.  Every dispatched call passes
        the cached session reference as the leading XAPI argument; when a
        call fails with ``SESSION_INVALID`` the manager re-logs-in
        transparently and retries the original call, bounded by
        ``aspects.max_attempts``.

        The transport is supplied through ``transport_factory`` so unit tests
        inject a fully mocked XML-RPC object and never contact a host.
    """

    def __init__(self, *, credential: XenSessionCredential,
                 transport_factory: Optional[
                     Callable[..., Any]] = None) -> None:
        """
            Construct an XenSessionManager.

            :param credential: The :class:`XenSessionCredential` to log in
                               with.
            :param transport_factory: Optional callable building the XML-RPC
                                      transport; defaults to the XAPI
                                      transport factory.

            :raises: ConfigurationError
        """
        if credential is None:
            err_msg = "XenSessionManager requires a XenSessionCredential."
            raise ConfigurationError(err_msg)

        self._credential: XenSessionCredential = credential
        self._transport_factory: Callable[..., Any] = (
            transport_factory if transport_factory is not None
            else _default_transport_factory
        )
        self._transport: Optional[Any] = None
        self._session_ref: Optional[str] = None
        return

    @property
    def session_ref(self) -> Optional[str]:
        """
            Return the cached session reference, or None before first login.

            :returns: The session reference string, or None.
        """
        rtnval = self._session_ref
        return rtnval

    def _ensure_transport(self) -> Any:
        """
            Return the XML-RPC transport, building it on first use.

            :returns: The transport object.
        """
        if self._transport is None:
            self._transport = self._transport_factory(
                master_url=self._credential.master_url)
        rtnval = self._transport
        return rtnval

    @staticmethod
    def _unwrap(*, response: Any) -> Any:
        """
            Unwrap an XAPI XML-RPC response envelope.

            :param response: The raw response dict (``{"Status": ...}``) or a
                             bare value.

            :returns: The ``Value`` payload on success.
            :raises: XenError
        """
        if not isinstance(response, dict):
            rtnval = response
            return rtnval

        status = response.get("Status", None)
        if status == "Success":
            rtnval = response.get("Value", None)
            return rtnval

        error_description = response.get("ErrorDescription", [])
        code = ""
        if isinstance(error_description, list) and len(error_description) > 0:
            code = str(error_description[0])

        err_msg_lines = ["XAPI call returned a failure status."]
        err_msg_lines.append("ERROR_DESCRIPTION: {!r}".format(
            error_description))
        err_msg = os.linesep.join(err_msg_lines)

        if code == SESSION_INVALID:
            raise XenError(err_msg)
        if code in _AUTH_FAILURE_CODES:
            raise XenAuthenticationError(err_msg)
        raise XenError(err_msg)

    @staticmethod
    def _is_session_invalid(*, xcpt: Exception) -> bool:
        """
            Report whether an exception is an XAPI ``SESSION_INVALID`` fault.

            :param xcpt: The raised exception.

            :returns: True when the fault is SESSION_INVALID.
        """
        rtnval = SESSION_INVALID in str(xcpt)
        return rtnval

    def login(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> str:
        """
            Perform ``session.login_with_password`` and cache the session.

            :param aspects: Behaviour controls.

            :returns: The session reference string.
            :raises: XenAuthenticationError
        """
        _ = aspects
        transport = self._ensure_transport()
        try:
            response = transport.session.login_with_password(
                self._credential.username, self._credential.password)
        except SemanticError:
            raise
        except Exception as xcpt:
            err_msg_lines = ["XAPI session.login_with_password raised."]
            err_msg_lines.append("MASTER_URL: {}".format(
                self._credential.master_url))
            err_msg_lines.append("CAUSE: {}".format(xcpt))
            err_msg = os.linesep.join(err_msg_lines)
            raise XenAuthenticationError(err_msg) from None

        session_ref = self._unwrap(response=response)
        self._session_ref = session_ref
        rtnval = session_ref
        return rtnval

    def logout(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Release the cached XAPI session.

            Idempotent: logging out when no session is held is a no-op.

            :param aspects: Behaviour controls.
        """
        _ = aspects
        if self._session_ref is None:
            return

        transport = self._ensure_transport()
        try:
            transport.session.logout(self._session_ref)
        except SemanticError:
            raise
        except Exception:
            # Logout is best-effort; a stale session simply expires.
            pass
        self._session_ref = None
        return

    def dispatch(self, *, method_path: str, args: Optional[List[Any]] = None,
                 aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> Any:
        """
            Dispatch an XAPI XML-RPC call, logging in transparently.

            The cached session reference is passed as the leading argument of
            every call.  When the call fails with ``SESSION_INVALID`` the
            manager re-logs-in and retries, bounded by
            ``aspects.max_attempts``.

            :param method_path: Dotted XAPI method path (e.g. ``VM.get_all``).
            :param args: Positional XAPI arguments after the session ref.
            :param aspects: Behaviour controls.

            :returns: The unwrapped XAPI ``Value`` payload.
            :raises: XenError, XenAuthenticationError
        """
        effective_args = args if args is not None else []
        max_attempts = aspects.max_attempts
        if max_attempts < 1:
            max_attempts = 1

        if self._session_ref is None:
            self.login(aspects=aspects)

        transport = self._ensure_transport()
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt < max_attempts:
            attempt = attempt + 1

            target = transport
            for part in method_path.split("."):
                target = getattr(target, part)

            call_args = [self._session_ref]
            call_args.extend(effective_args)

            try:
                response = target(*call_args)
                rtnval = self._unwrap(response=response)
                return rtnval
            except XenAuthenticationError:
                raise
            except SemanticError:
                raise
            except Exception as xcpt:
                last_error = xcpt
                if self._is_session_invalid(xcpt=xcpt) and attempt < max_attempts:
                    self._session_ref = None
                    self.login(aspects=aspects)
                    continue
                raise

        err_msg_lines = ["XAPI dispatch exhausted its attempt budget."]
        err_msg_lines.append("METHOD: {}".format(method_path))
        err_msg_lines.append("ATTEMPTS: {}".format(max_attempts))
        err_msg_lines.append("LAST_ERROR: {}".format(last_error))
        err_msg = os.linesep.join(err_msg_lines)
        raise XenError(err_msg)
