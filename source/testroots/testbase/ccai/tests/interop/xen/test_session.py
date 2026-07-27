"""
    .. module:: test_session
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Session login / logout / transparent-re-login tests for the
        Xen interop client.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from ccai import testbase


from ccai.errors.exceptions import ConfigurationError, SemanticError

from ccai.interop.xen.exceptions.xenexceptions import (
    XenAuthenticationError
)
from ccai.interop.xen.session.xensessioncredential import (
    XenSessionCredential
)
from ccai.interop.xen.xenclient import XenClient

from ._mockxapi import MockXapiTransport


def test_credential_rejects_missing_fields() -> None:
    """
        Missing pool-master URL or credentials raises ConfigurationError.
    """
    with testbase.raises(ConfigurationError):
        XenSessionCredential(master_url="", username="root",
                             password="secret")
    return


def test_login_caches_session(client, transport, fast_aspects) -> None:
    """
        First use logs in once and caches the session reference.
    """
    client.login(aspects=fast_aspects)
    assert client.session_manager.session_ref is not None
    assert transport.login_count == 1
    return


def test_login_failure_raises_authentication_error(credential,
                                                   fast_aspects) -> None:
    """
        A rejected login raises XenAuthenticationError.
    """
    transport = MockXapiTransport(reject_login=True)
    client = XenClient(credential=credential,
                       transport_factory=lambda *, master_url: transport,
                       aspects=fast_aspects)
    with testbase.raises(XenAuthenticationError):
        client.login(aspects=fast_aspects)
    return


def test_logout_releases_session(client, fast_aspects) -> None:
    """
        Logout clears the cached session and is idempotent.
    """
    client.login(aspects=fast_aspects)
    client.logout(aspects=fast_aspects)
    assert client.session_manager.session_ref is None
    client.logout(aspects=fast_aspects)
    return


def test_transparent_relogin_on_session_invalid(client, transport,
                                                fast_aspects) -> None:
    """
        A SESSION_INVALID fault triggers a transparent re-login and retry;
        the call's observable result matches the single-login case.
    """
    client.login(aspects=fast_aspects)
    # Fail the next non-session call once.
    transport.session_invalid_on_call = transport._non_session_calls + 1

    hosts = client.Hosts.list(aspects=fast_aspects)
    assert len(hosts) == 1
    # One initial login plus one re-login.
    assert transport.login_count == 2
    return


def test_relogin_equivalence_across_first_call(credential,
                                               fast_aspects) -> None:
    """
        Even when the very first dispatched call hits SESSION_INVALID, the
        result equals the no-failure case.
    """
    transport = MockXapiTransport()
    transport.session_invalid_on_call = 1
    client = XenClient(credential=credential,
                       transport_factory=lambda *, master_url: transport,
                       aspects=fast_aspects)
    hosts = client.Hosts.list(aspects=fast_aspects)
    assert len(hosts) == 1
    return


class _SemanticRaisingTransport(MockXapiTransport):
    """
        A transport whose XAPI object dispatch raises SemanticError so the
        session manager's exception discipline can be verified.
    """

    def _dispatch_xapi(self, method_path: str, args: tuple):
        """
            Raise a SemanticError instead of dispatching the call.
        """
        raise SemanticError("injected semantic error")


def test_dispatch_lets_semantic_error_bubble(credential,
                                             fast_aspects) -> None:
    """
        A SemanticError raised within a dispatched call must bubble out of
        ``dispatch`` unchanged — never reclassified as XenError and never
        consumed by the SESSION_INVALID retry loop.
    """
    transport = _SemanticRaisingTransport()
    client = XenClient(credential=credential,
                       transport_factory=lambda *, master_url: transport,
                       aspects=fast_aspects)
    client.login(aspects=fast_aspects)
    with testbase.raises(SemanticError):
        client.session_manager.dispatch(method_path="VM.get_all_records",
                                        aspects=fast_aspects)
    return
