"""
    .. module:: test_transport
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: XML-RPC transport envelope unwrapping and error-handling
        tests for the XenSessionManager dispatch path.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from ccai import testbase


from ccai.errors.exceptions import ConfigurationError

from ccai.interop.xen.exceptions.xenexceptions import (
    XenAuthenticationError, XenError
)
from ccai.interop.xen.session.xensessionmanager import XenSessionManager


def test_unwrap_returns_bare_value() -> None:
    """
        A bare (non-dict) response is returned unchanged.
    """
    value = XenSessionManager._unwrap(response="bare-string")
    assert value == "bare-string"
    return


def test_unwrap_success_returns_value() -> None:
    """
        A success envelope yields its Value payload.
    """
    value = XenSessionManager._unwrap(
        response={"Status": "Success", "Value": [1, 2, 3]})
    assert value == [1, 2, 3]
    return


def test_unwrap_failure_raises_xen_error() -> None:
    """
        A generic failure envelope raises XenError.
    """
    with testbase.raises(XenError):
        XenSessionManager._unwrap(
            response={"Status": "Failure",
                      "ErrorDescription": ["INTERNAL_ERROR", "boom"]})
    return


def test_unwrap_auth_failure_raises_authentication_error() -> None:
    """
        An authentication failure code reclassifies to
        XenAuthenticationError.
    """
    with testbase.raises(XenAuthenticationError):
        XenSessionManager._unwrap(
            response={"Status": "Failure",
                      "ErrorDescription": ["SESSION_AUTHENTICATION_FAILED"]})
    return


def test_is_session_invalid_detects_marker() -> None:
    """
        _is_session_invalid is true only when the SESSION_INVALID marker is
        present in the exception text.
    """
    invalid = XenError("XAPI failure: SESSION_INVALID happened")
    other = XenError("XAPI failure: HANDLE_INVALID happened")
    assert XenSessionManager._is_session_invalid(xcpt=invalid) is True
    assert XenSessionManager._is_session_invalid(xcpt=other) is False
    return


def test_session_manager_requires_credential() -> None:
    """
        Constructing a XenSessionManager without a credential raises
        ConfigurationError.
    """
    with testbase.raises(ConfigurationError):
        XenSessionManager(credential=None)
    return


def test_dispatch_unknown_method_raises_xen_error(client,
                                                  fast_aspects) -> None:
    """
        An unknown XAPI method dispatched through the manager raises
        XenError after exhausting the attempt budget or immediately.
    """
    with testbase.raises(XenError):
        client.session_manager.dispatch(method_path="VM.no_such_method",
                                        args=[], aspects=fast_aspects)
    return


def test_dispatch_logs_in_before_first_call(client, transport,
                                            fast_aspects) -> None:
    """
        The first dispatched call logs in transparently before dispatching.
    """
    assert client.session_manager.session_ref is None
    client.Hosts.list(aspects=fast_aspects)
    assert client.session_manager.session_ref is not None
    assert transport.login_count == 1
    return
